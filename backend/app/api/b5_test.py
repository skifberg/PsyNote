from flask import Blueprint, request, jsonify
import json
import os
from flask_cors import CORS

b5_test_bp = Blueprint('b5_test', __name__)
CORS(b5_test_bp, origins=["http://localhost:8000"])  # Явно указываем порт 8000

# Путь к файлу с вопросами
QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'b5_questions.json')

@b5_test_bp.route('/api/b5-test/questions', methods=['GET'])
def get_b5_questions():
    """Получить все вопросы теста"""
    try:
        with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        return jsonify({
            "success": True, 
            "questions": questions,
            "total": len(questions)
        })
    except FileNotFoundError:
        return jsonify({
            "success": False, 
            "message": "Файл с вопросами не найден"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Ошибка при загрузке вопросов: {str(e)}"
        }), 500

@b5_test_bp.route('/api/b5-test/submit', methods=['POST'])
def submit_answers():
    """Обработать ответы и вернуть результаты"""
    try:
        data = request.get_json()
        
        if not data or 'answers' not in data:
            return jsonify({
                "success": False,
                "message": "Отсутствуют данные ответов"
            }), 400
        
        answers = data['answers']
        results = calculate_scores(answers)
        
        return jsonify({
            "success": True,
            "scores": results,
            "interpretation": interpret_scores(results)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Ошибка обработки ответов: {str(e)}"
        }), 500

def calculate_scores(answers):
    """Рассчитать баллы по каждому фактору"""
    factors = {'E': 0, 'A': 0, 'C': 0, 'N': 0, 'O': 0}
    
    try:
        with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
        
        questions_dict = {q['id']: q for q in questions_data}
        
        for answer in answers:
            question_id = answer['questionId']
            answer_value = answer['answerValue']
            
            question = questions_dict.get(question_id)
            if question:
                factor = question['factor']
                is_reversed = question['is_reversed']
                
                final_value = (6 - answer_value) if is_reversed else answer_value
                factors[factor] += final_value
        
        return factors
        
    except Exception as e:
        raise Exception(f"Error calculating scores: {str(e)}")

def interpret_scores(scores):
    """Интерпретировать результаты"""
    interpretations = {
        'E': {
            'high': 'Вы общительны, энергичны и получаете энергию от взаимодействия с людьми.',
            'medium': 'Вы находите баланс между общением и временем наедине с собой.',
            'low': 'Вы более сдержанны, цените уединение и глубокие размышления.'
        },
        'A': {
            'high': 'Вы добры, отзывчивы и стремитесь к гармонии в отношениях.',
            'medium': 'Вы находите баланс между помощью другим и защитой своих интересов.',
            'low': 'Вы более скептичны, прямолинейны и ориентированы на собственные цели.'
        },
        'C': {
            'high': 'Вы организованны, дисциплинированны и надежны.',
            'medium': 'Вы сочетаете организованность с гибкостью.',
            'low': 'Вы спонтанны и гибки, не любите жестких рамок.'
        },
        'N': {
            'high': 'Вы эмоционально чувствительны, глубоко переживаете события.',
            'medium': 'Вы в целом эмоционально устойчивы.',
            'low': 'Вы эмоционально стабильны, спокойны и уверены в себе.'
        },
        'O': {
            'high': 'Вы любознательны, креативны и открыты новому.',
            'medium': 'Вы сочетаете интерес к новому с практичностью.',
            'low': 'Вы практичны, реалистичны и консервативны.'
        }
    }
    
    result = {}
    for factor, score in scores.items():
        if score >= 36:
            level = 'high'
        elif score >= 26:
            level = 'medium'
        else:
            level = 'low'
        
        result[factor] = {
            'score': score,
            'level': level,
            'interpretation': interpretations[factor][level],
            'max_score': 50
        }
    
    return result