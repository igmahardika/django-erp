from django.db import models


class RecruitmentStatus(models.Model):
    stat_name = models.CharField(max_length=30, unique=True)
    stat_order = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return self.stat_name + " (" + self.stat_order.__str__() + ")"

    @staticmethod
    def get_max_id():
        statuses = RecruitmentStatus.objects.all()
        max_id = 0
        for status in statuses:
            if status.stat_order > max_id:
                max_id = status.stat_order
        return max_id


class JobOffer(models.Model):
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]
    NCAL_CHOICES = [
        ("Blue", "Blue"),
        ("Yellow", "Yellow"),
        ("Orange", "Orange"),
        ("Red", "Red"),
        ("Black", "Black"),
    ]
    priority = models.CharField(max_length=10, blank=True, null=True, choices=PRIORITY_CHOICES, verbose_name="Priority (Tingkat urgensi gangguan)")
    site_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Site (Nama lokasi pelanggan)")
    case_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="No Case (Nomor kasus/laporan gangguan)")
    customer = models.CharField(max_length=100, blank=True, null=True, choices=NCAL_CHOICES, verbose_name="NCAL (Nama pelanggan/akun)")
    status = models.CharField(max_length=50, blank=True, null=True, verbose_name="Status (Status penanganan)")
    severity_level = models.CharField(max_length=50, blank=True, null=True, verbose_name="Level (Level/skala gangguan)")
    technician = models.CharField(max_length=100, blank=True, null=True, verbose_name="TS (Teknisi yang menangani)")
    segmen = models.CharField(max_length=100, blank=True, null=True, verbose_name="Segmen")
    start_time = models.DateTimeField(blank=True, null=True, verbose_name="Start (Tanggal & waktu mulai gangguan)")
    start_escalation_waneda = models.DateTimeField(blank=True, null=True, verbose_name="Start Escalation (waneda)")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="End (Waktu gangguan selesai)")
    duration = models.DurationField(blank=True, null=True, verbose_name="Duration (Lama gangguan)")
    duration_waneda = models.DurationField(blank=True, null=True, verbose_name="Duration (waneda)")
    problem_summary = models.TextField(blank=True, null=True, verbose_name="Problem (Ringkasan masalah)")
    root_cause = models.TextField(blank=True, null=True, verbose_name="Penyebab (Penyebab gangguan)")
    last_action = models.TextField(blank=True, null=True, verbose_name="Action Terakhir (Langkah terakhir)")
    note = models.TextField(blank=True, null=True, verbose_name="Note (Catatan tambahan)")
    issue_classification = models.CharField(max_length=100, blank=True, null=True, verbose_name="Klasifikasi Gangguan (Kategori teknis)")
    power_before = models.CharField(max_length=50, blank=True, null=True, verbose_name="Power Before (Status daya sebelum)")
    power_after = models.CharField(max_length=50, blank=True, null=True, verbose_name="Power After (Status daya sesudah)")
    start_pause_time = models.DateTimeField(blank=True, null=True, verbose_name="Start Pause (Waktu jeda mulai)")
    end_pause_time = models.DateTimeField(blank=True, null=True, verbose_name="End Pause (Waktu jeda selesai)")
    pause_duration = models.DurationField(blank=True, null=True, verbose_name="Duration Pause (Durasi jeda)")
    actual_handling_duration = models.DurationField(blank=True, null=True, verbose_name="Duration Penanganan Real (Waktu real penanganan)")
    is_closed = models.BooleanField(default=False, verbose_name="Closed")
    close_time = models.DateTimeField(blank=True, null=True, verbose_name="Close Time")
    close_duration = models.DurationField(blank=True, null=True, verbose_name="Durasi Close Trouble")
    close_escalation_duration = models.DurationField(blank=True, null=True, verbose_name="Durasi Close Eskalasi Vendor")

    class Meta:
        verbose_name = "Current Trouble"
        verbose_name_plural = "Current Troubles"

    def __unicode__(self):
        return self.case_number or str(self.id)


class JobApplicant(models.Model):
    appl_name = models.CharField(max_length=50, verbose_name="Trouble done")
    appl_surname = models.CharField(max_length=100, verbose_name="Applicant surname")
    appl_email = models.EmailField(max_length=100, verbose_name="Applicant email")
    appl_address = models.CharField(max_length=200, verbose_name="Applicant address")
    appl_phone = models.CharField(max_length=15, verbose_name="Applicant phone")
    appl_birthdate = models.DateField(verbose_name="Applicant birthday")
    appl_submitted = models.DateTimeField(auto_now=True)
    appl_status = models.ForeignKey(RecruitmentStatus, verbose_name="Applicant status", on_delete=models.CASCADE)
    appl_job = models.ForeignKey(JobOffer, verbose_name="Applies for", on_delete=models.CASCADE)
    appl_notes = models.TextField(default="", max_length=1500, verbose_name="Other notes", blank=True, null=True)

    class Meta:
        verbose_name = "Trouble done"
        verbose_name_plural = "Trouble done"

    def get_string(self):
        return self.appl_name + " " + self.appl_surname

    def __unicode__(self):
        return self.get_string()

    def __str__(self):
        return self.get_string()


class Employee(models.Model):
    emp_applicant = models.ForeignKey(JobApplicant, verbose_name="Applicant", on_delete=models.CASCADE)
    emp_salary = models.IntegerField(verbose_name="Salary ($)")
    emp_position = models.CharField(max_length=50, verbose_name="History Trouble")

    class Meta:
        verbose_name = "History Trouble"
        verbose_name_plural = "History Troubles"

    def get_string(self):
        return self.emp_applicant.appl_name + " " + self.emp_applicant.appl_surname

    def __unicode__(self):
        return self.emp_applicant.__str__()


class SalaryHistory(models.Model):
    shi_employee = models.ForeignKey(Employee, verbose_name="Employee", on_delete=models.SET_NULL, null=True)
    shi_salary = models.IntegerField(verbose_name="Salary ($)")
    shi_month = models.DateField(verbose_name="Payday")

    def __str__(self):
        return self.shi_employee.get_string()


class JobUpdateHistory(models.Model):
    job = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name='update_histories')
    technical_support = models.CharField(max_length=100, verbose_name="Technical Support")
    penyebab = models.TextField(verbose_name="Penyebab")
    action = models.TextField(verbose_name="Action")
    start_escalation_vendor = models.DateTimeField(verbose_name="Start Eskalasi ke Vendor", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Update by {self.technical_support} at {self.created_at}";