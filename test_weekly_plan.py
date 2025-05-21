#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para crear un plan semanal de prueba y verificar la lista de compras
"""

from bson import ObjectId
from repositories.mongo_connection import db
import sys

def create_test_recipes():
    """Crea recetas de prueba"""
    recipes = [
        {
            "name": "Ensalada César",
            "description": "Ensalada clásica con pollo y aderezo césar",
            "ingredients": [
                {"name": "lechuga", "quantity": 1, "unit": "unidad"},
                {"name": "pollo", "quantity": 200, "unit": "g"},
                {"name": "queso parmesano", "quantity": 50, "unit": "g"},
                {"name": "aderezo césar", "quantity": 30, "unit": "ml"}
            ]
        },
        {
            "name": "Pasta al Pesto",
            "description": "Pasta con salsa pesto casera",
            "ingredients": [
                {"name": "pasta", "quantity": 200, "unit": "g"},
                {"name": "albahaca", "quantity": 30, "unit": "g"},
                {"name": "piñones", "quantity": 20, "unit": "g"},
                {"name": "queso parmesano", "quantity": 30, "unit": "g"},
                {"name": "aceite de oliva", "quantity": 50, "unit": "ml"}
            ]
        },
        {
            "name": "Smoothie de Frutas",
            "description": "Batido de frutas y yogurt",
            "ingredients": [
                {"name": "plátano", "quantity": 1, "unit": "unidad"},
                {"name": "fresa", "quantity": 100, "unit": "g"},
                {"name": "yogurt", "quantity": 150, "unit": "ml"},
                {"name": "miel", "quantity": 15, "unit": "ml"}
            ]
        }
    ]
    
    recipe_ids = []
    for recipe in recipes:
        result = db.recipes.insert_one(recipe)
        recipe_ids.append(str(result.inserted_id))
        print(f"Receta '{recipe['name']}' creada con ID: {result.inserted_id}")
    
    return recipe_ids

def create_weekly_plan(user_id_str):
    """Crea o actualiza un plan semanal para el usuario"""
    try:
        # El problema es que el ID del usuario no se está convirtiendo correctamente a ObjectId
        # Imprimir información para depuración
        print(f"ID de usuario recibido: {user_id_str}, tipo: {type(user_id_str)}")
        
        # Convertir el user_id a ObjectId
        try:
            user_id_obj = ObjectId(user_id_str)
            print(f"ObjectId creado: {user_id_obj}")
        except Exception as e:
            print(f"Error al convertir a ObjectId: {e}")
            return
            
        # Verificar si ya existe un plan semanal
        existing_plan = db.weekly_plans.find_one({"user_id": user_id_obj})
        
        if existing_plan:
            print(f"Plan semanal existente: {existing_plan}")
            # Eliminar plan existente para crear uno nuevo
            db.weekly_plans.delete_one({"_id": existing_plan["_id"]})
            print(f"Plan semanal anterior eliminado")
        
        # Crear recetas de prueba
        recipe_ids = create_test_recipes()
        
        # Crear documento de plan semanal
        plan = {
            "user_id": user_id_obj,
            "recipes": recipe_ids,
            "week": "current"
        }
        
        # Insertar en la base de datos
        result = db.weekly_plans.insert_one(plan)
        print(f"Nuevo plan semanal creado con ID: {result.inserted_id}")
        
        # Verificar si fue insertado correctamente
        inserted_plan = db.weekly_plans.find_one({"_id": result.inserted_id})
        print(f"Plan insertado: {inserted_plan}")
        
        # Ahora intentar obtener el plan por user_id
        fetched_plan = db.weekly_plans.find_one({"user_id": user_id_obj})
        print(f"Plan obtenido por user_id: {fetched_plan}")
        
        # También probar obtener por string
        fetched_plan_str = db.weekly_plans.find_one({"user_id": user_id_str})
        print(f"Plan obtenido por user_id como string: {fetched_plan_str}")
        
        return str(result.inserted_id)
        
    except Exception as e:
        print(f"Error general al crear plan semanal: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
    else:
        user_id = input("Ingrese el ID de usuario: ")
    
    print(f"Creando plan semanal para usuario: {user_id}")
    plan_id = create_weekly_plan(user_id)
    
    if plan_id:
        print(f"Plan semanal creado exitosamente con ID: {plan_id}")
    else:
        print("No se pudo crear el plan semanal.") 