from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    # ── List view ────────────────────────────────────────────
    list_display = ("title", "company", "field", "short_skills", "updated_at")
    list_filter = ("field",)
    search_fields = ("title", "company", "field", "skills", "description")
    ordering = ("field", "title")

    # ── Detail / edit view ───────────────────────────────────
    fieldsets = (
        ("Job Details", {
            "fields": ("title", "company", "field"),
        }),
        ("Content", {
            "fields": ("description", "skills"),
            "description": (
                "The description and skills are combined and embedded into "
                "a vector for semantic search. Be descriptive for better matching."
            ),
        }),
    )

    readonly_fields = ("chroma_id", "created_at", "updated_at")

    # ── Custom column ────────────────────────────────────────
    @admin.display(description="Skills (preview)")
    def short_skills(self, obj):
        return obj.skills[:60] + "..." if len(obj.skills) > 60 else obj.skills

    # ── Admin actions ────────────────────────────────────────
    actions = ["resync_to_chroma"]

    @admin.action(description="Re-sync selected jobs to ChromaDB")
    def resync_to_chroma(self, request, queryset):
        count = 0
        for job in queryset:
            job.sync_to_chroma()
            job.save()
            count += 1
        self.message_user(request, f"✓ Successfully re-synced {count} job(s) to ChromaDB.")
