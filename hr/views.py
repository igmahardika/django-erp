__author__ = 'tomasz'

from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from hr.models import JobApplicant, JobOffer, Employee, JobUpdateHistory
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone


@login_required
def index(request):
    # Count open JobOffer for each NCAL
    ncal_colors = ['Blue', 'Yellow', 'Orange', 'Red', 'Black']
    ncal_counts = {color: JobOffer.objects.filter(is_closed=False, customer=color).count() for color in ncal_colors}
    total_open = JobOffer.objects.filter(is_closed=False).count()
    context = {
        'ncal_counts': ncal_counts,
        'total_open': total_open,
    }
    return render(request, "hr/index.html", context)


@login_required
def jobs(request):
    if request.method == 'POST':
        JobOffer.objects.create(
            priority=request.POST.get('priority'),
            site_id=request.POST.get('site_id'),
            case_number=request.POST.get('case_number'),
            customer=request.POST.get('customer'),
            segmen=request.POST.get('segmen'),
            start_time=request.POST.get('start_time') or None,
            problem_summary=request.POST.get('problem_summary'),
        )
        return redirect('hr:jobs')
    now = timezone.now()
    ncal_targets = {
        'Blue': 6,
        'Yellow': 5,
        'Orange': 3,
        'Red': 2,
        'Black': 1,
    }
    job_qs = JobOffer.objects.filter(is_closed=False).order_by('-start_time')
    job_list = []
    for job in job_qs:
        open_duration_str = None
        level = None
        duration_alert = False
        if job.start_time:
            start_time = job.start_time
            if timezone.is_naive(start_time):
                start_time = timezone.make_aware(start_time, timezone.get_current_timezone())
            end_time = job.close_time if getattr(job, 'is_closed', False) and job.close_time else now
            open_duration = end_time - start_time
            # Always use absolute value for display
            abs_duration = abs(open_duration)
            total_seconds = int(abs_duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            open_duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            level = hours + 1
            target = ncal_targets.get(job.customer, None)
            if target and hours > target:
                duration_alert = True
        job_list.append({
            'id': job.id,
            'priority': job.priority,
            'site_id': job.site_id,
            'case_number': job.case_number,
            'customer': job.customer,
            'segmen': job.segmen,
            'start_time': job.start_time,
            'problem_summary': job.problem_summary,
            'open_duration': open_duration_str,
            'level': level,
            'duration_alert': duration_alert,
        })
    context = {'job_list': job_list}
    return render(request, "hr/job_list.html", context)


@login_required
def job(request, job_id):
    selected_job = get_object_or_404(JobOffer, pk=job_id)
    applicant_list = JobApplicant.objects.filter(appl_job=job_id)
    # Prepare update histories with duration and level
    update_histories = []
    if selected_job.start_time:
        start_time = selected_job.start_time
        if timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time, timezone.get_current_timezone())
        for update in selected_job.update_histories.order_by('created_at'):
            update_time = update.created_at
            if timezone.is_naive(update_time):
                update_time = timezone.make_aware(update_time, timezone.get_current_timezone())
            duration = abs(update_time - start_time)
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            level = hours + 1
            update_histories.append({
                'technical_support': update.technical_support,
                'penyebab': update.penyebab,
                'action': update.action,
                'start_escalation_vendor': update.start_escalation_vendor,
                'created_at': update.created_at,
                'duration': duration_str,
                'level': level,
            })
    context = {'job': selected_job, 'applicants': applicant_list, 'update_histories': update_histories}
    return render(request, "hr/job.html", context)


@login_required
def applicants(request):
    job_list = JobOffer.objects.filter(is_closed=True).order_by('-start_time').values('id', 'priority', 'site_id', 'case_number', 'customer', 'segmen', 'start_time', 'problem_summary')
    context = {'job_list': job_list}
    return render(request, "hr/applicants.html", context)


@login_required
def applicant(request, app_id):
    selected_applicant = get_object_or_404(JobApplicant, pk=app_id)
    context = {'applicant': selected_applicant}
    return render(request, "hr/applicant.html", context)


@login_required
def employees(request):
    employee_list = Employee.objects.order_by('-emp_salary')
    context = {'employee_list': employee_list}
    return render(request, "hr/employees.html", context)


@login_required
def employee(request, emp_id):
    selected_employee = get_object_or_404(Employee, pk=emp_id)
    context = {'employee': selected_employee}
    return render(request, "hr/employee.html", context)


@login_required
def logout_user(request):
    logout(request)
    return render(request, "hr/logout.html")


@login_required
def update_job(request, job_id):
    job = get_object_or_404(JobOffer, pk=job_id)
    if request.method == 'POST':
        if 'close' in request.POST:
            now = timezone.now()
            job.is_closed = True
            job.close_time = now
            if job.start_time:
                # Ensure both are aware
                start_time = job.start_time
                if timezone.is_naive(start_time):
                    start_time = timezone.make_aware(start_time, timezone.get_current_timezone())
                job.close_duration = now - start_time
            # Cari start eskalasi vendor terakhir dari history
            last_history = job.update_histories.order_by('-created_at').first()
            if last_history and last_history.start_escalation_vendor:
                eskalasi_time = last_history.start_escalation_vendor
                if timezone.is_naive(eskalasi_time):
                    eskalasi_time = timezone.make_aware(eskalasi_time, timezone.get_current_timezone())
                job.close_escalation_duration = now - eskalasi_time
            job.save()
            return redirect('hr:applicants')
        else:
            JobUpdateHistory.objects.create(
                job=job,
                technical_support=request.POST.get('technical_support'),
                penyebab=request.POST.get('penyebab'),
                action=request.POST.get('action'),
                start_escalation_vendor=request.POST.get('start_escalation_vendor') or None,
            )
            return render(request, 'hr/update_job.html', {'job': job, 'success': True, 'update_histories': job.update_histories.all()})
    return render(request, 'hr/update_job.html', {'job': job, 'update_histories': job.update_histories.all()})

