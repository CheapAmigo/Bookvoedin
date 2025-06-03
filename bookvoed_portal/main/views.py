from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, LoginForm, BookCardForm
from .models import BookCard
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Неверный логин или пароль. Пожалуйста, попробуйте снова.')
        
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user_cards = BookCard.objects.filter(user=request.user).exclude(status='archived')
    archived_cards = BookCard.objects.filter(user=request.user, status='archived')
    return render(request, 'main/profile.html', {
        'user_cards': user_cards,
        'archived_cards': archived_cards
    })

@login_required
def create_card_view(request):
    if request.method == 'POST':
        form = BookCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('profile')
    else:
        form = BookCardForm()
    return render(request, 'main/create_card.html', {'form': form})

@login_required
def delete_card_view(request, card_id):
    card = get_object_or_404(BookCard, id=card_id, user=request.user)
    if request.method == 'POST':
        card.status = 'archived'
        card.save()
        return redirect('profile')
    return render(request, 'main/confirm_delete.html', {'card': card})

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_panel_view(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        action = request.POST.get('action')
        reason = request.POST.get('reason', '')
        card = get_object_or_404(BookCard, id=card_id)
        
        if action == 'approve':
            card.status = 'approved'
        elif action == 'reject':
            card.status = 'rejected'
            card.rejection_reason = reason
        card.save()
    
    pending_cards = BookCard.objects.filter(status='pending')
    return render(request, 'main/admin_panel.html', {'pending_cards': pending_cards})