from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, UserScore
from django.http import HttpResponse

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz_detail.html', {'quiz': quiz, 'questions': questions})

def submit_quiz(request, quiz_id):
    if request.method == "POST":
        print("Form submitted")
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        score = 0

        for question in questions:
            selected_option = request.POST.get(f'q{question.id}')
            print(f'Question ID: {question.id}, Selected Option: {selected_option}')  
            if selected_option and int(selected_option) == question.correct_option:
                score += 1

        print(f'Score: {score}')  
        UserScore.objects.create(user=request.user, quiz=quiz, score=score)
        return HttpResponse(f"You scored {score} out of {questions.count()}!")
    
    return HttpResponse("Invalid request")


def leaderboard(request):
    scores = UserScore.objects.order_by('-score')[:10]
    return render(request, 'quiz/leaderboard.html', {'scores': scores})

def quiz_result(request, quiz_id, score):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score})

