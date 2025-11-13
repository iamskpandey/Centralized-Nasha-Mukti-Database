from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from .forms import BeneficiaryForm, InterventionForm
from .models import Beneficiary, Intervention, Center

@login_required
def home(request):
    user_profile = request.user.userprofile
    
    if user_profile.role == 'super_admin':
        beneficiary_query = Beneficiary.objects.all()
        intervention_query = Intervention.objects.all()
        center_query = Center.objects.all()

    elif user_profile.role == 'state_admin':
        user_state = user_profile.state
        beneficiary_query = Beneficiary.objects.filter(center__state=user_state)
        intervention_query = Intervention.objects.filter(beneficiary__center__state=user_state)
        center_query = Center.objects.filter(state=user_state)
        
    else: 
        user_center = user_profile.center
        
        beneficiary_query = Beneficiary.objects.filter(center=user_center)
        
        intervention_query = Intervention.objects.filter(beneficiary__center=user_center)
        
        center_query = Center.objects.filter(pk=user_center.pk)

    total_beneficiaries = beneficiary_query.count()
    total_interventions = intervention_query.count()
    total_centers = center_query.count() # This will be 1 for staff

    recent_interventions = intervention_query.order_by('-date_of_intervention')[:5]

    context = {
        'total_beneficiaries': total_beneficiaries,
        'total_interventions': total_interventions,
        'total_centers': total_centers,
        'recent_interventions': recent_interventions,
    }
    return render(request, 'registry/home.html', context)

@login_required
def add_beneficiary(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, user=request.user)
        if form.is_valid():
            beneficiary = form.save(commit=False)
            if user_profile.role == 'center_staff':
                if not user_profile.center:
                    form.add_error(None, "Your user account is not assigned to a center. Please contact an administrator.")
                    return render(request, 'registry/beneficiary_form.html', {'form': form})
                beneficiary.center = user_profile.center
            beneficiary.save()
            return redirect('home')
    else:
        form = BeneficiaryForm(user=request.user)

    return render(request, 'registry/beneficiary_form.html', {'form': form})

@login_required
def beneficiary_list(request):
    user_profile = request.user.userprofile
    
    if user_profile.role == 'super_admin':
        beneficiaries = Beneficiary.objects.all().order_by('name')

    elif user_profile.role == 'state_admin':
        beneficiaries = Beneficiary.objects.filter(
            center__state=user_profile.state
        ).order_by('name')

    else:
        beneficiaries = Beneficiary.objects.filter(
            center=user_profile.center
        ).order_by('name')
    
    paginator = Paginator(beneficiaries, 25) 

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'registry/beneficiary_list.html', context)

@login_required
def beneficiary_detail(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    
    if request.method == 'POST':
        form = InterventionForm(request.POST)
        if form.is_valid():
            intervention = form.save(commit=False) 
            intervention.beneficiary = beneficiary 
            intervention.staff_member = request.user 
            intervention.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = InterventionForm()

    interventions = Intervention.objects.filter(
        beneficiary=beneficiary
    )

    context = {
        'beneficiary': beneficiary,
        'interventions': interventions,
        'form': form, 
    }
    return render(request, 'registry/beneficiary_detail.html', context)

@login_required
def reports_page(request):
    user_profile = request.user.userprofile
    centers_query = Center.objects.all()
    if user_profile.role == 'center_staff':
        centers_query = centers_query.filter(pk=user_profile.center.pk)
    
    elif user_profile.role == 'state_admin':
        centers_query = centers_query.filter(state=user_profile.state)
    
    centers_data = centers_query.annotate(
        beneficiary_count=Count('beneficiary', distinct=True),
        
        intervention_count=Count('beneficiary__intervention', distinct=True)
    ).order_by('-beneficiary_count') 

    context = {
        'centers_data': centers_data
    }
    return render(request, 'registry/reports_page.html', context)

@login_required
def edit_beneficiary(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    user_profile = request.user.userprofile
    
    if (user_profile.role == 'center_staff' and user_profile.center != beneficiary.center):
        return redirect('home')

    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, instance=beneficiary, user =request.user)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = BeneficiaryForm(instance=beneficiary, user=request.user)

    context = {
        'form': form,
        'beneficiary': beneficiary
    }
    return render(request, 'registry/beneficiary_edit_form.html', context)

@login_required
def delete_beneficiary(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    user_profile = request.user.userprofile

    if (user_profile.role == 'center_staff' and
        user_profile.center != beneficiary.center):
        return redirect('home')

    if request.method == 'POST':
        beneficiary.delete()
        return redirect('beneficiary_list')

    context = {
        'beneficiary': beneficiary
    }
    return render(request, 'registry/beneficiary_delete_confirm.html', context)

@login_required
def edit_intervention(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    beneficiary = intervention.beneficiary
    user_profile = request.user.userprofile

    if (user_profile.role == 'center_staff' and
        user_profile.center != beneficiary.center):
        return redirect('home')

    if request.method == 'POST':
        form = InterventionForm(request.POST, instance=intervention)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = InterventionForm(instance=intervention)

    context = {
        'form': form,
        'intervention': intervention,
        'beneficiary': beneficiary, 
    }
    return render(request, 'registry/intervention_edit_form.html', context)

@login_required
def delete_intervention(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    beneficiary = intervention.beneficiary
    user_profile = request.user.userprofile

    if (user_profile.role == 'center_staff' and
        user_profile.center != beneficiary.center):
        return redirect('home')
    
    if request.method == 'POST':
        intervention.delete()
        return redirect('beneficiary_detail', pk=beneficiary.pk)

    context = {
        'intervention': intervention,
        'beneficiary': beneficiary,
    }
    return render(request, 'registry/intervention_delete_confirm.html', context)

@login_required
def intervention_history(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    user_profile = request.user.userprofile
    
    if user_profile.role == 'center_staff' and user_profile.center != beneficiary.center:
        return redirect('home')
    elif user_profile.role == 'state_admin' and beneficiary.center.state != user_profile.state:
        return redirect('home')
    
    interventions = Intervention.objects.filter(
        beneficiary=beneficiary
    ).order_by('-date_of_intervention')
    
    context = {
        'beneficiary': beneficiary,
        'interventions': interventions,
    }
    return render(request, 'registry/intervention_history.html', context)