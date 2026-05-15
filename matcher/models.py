import uuid
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Job(models.Model):
    """
    Represents a job listing.
    Jobs are stored in Django's SQLite DB (for admin management)
    AND automatically synced to ChromaDB (for vector search).
    """

    title = models.CharField(max_length=200, help_text="Job title, e.g. Software Engineer")
    company = models.CharField(max_length=200, help_text="Company name")
    field = models.CharField(max_length=100, help_text="Industry/field, e.g. Healthcare")
    description = models.TextField(help_text="Full job description")
    skills = models.CharField(
        max_length=500,
        help_text="Comma-separated required skills, e.g. Python, SQL, Git",
    )
    # Stores the ChromaDB vector ID so we can update/delete it
    chroma_id = models.CharField(max_length=100, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["field", "title"]
        verbose_name = "Job Listing"
        verbose_name_plural = "Job Listings"

    def __str__(self):
        return f"{self.title} @ {self.company} ({self.field})"

    def get_embed_text(self):
        """Build the rich text that gets embedded into a vector."""
        return (
            f"{self.title} in {self.field}. "
            f"{self.description} "
            f"Required skills: {self.skills}"
        )

    def sync_to_chroma(self):
        """
        Embed this job and upsert it into ChromaDB.
        Uses upsert so both new and edited jobs are handled.
        """
        from matcher.vector_db import get_jobs_collection, embed_text

        # Assign a stable ChromaDB ID if not already set
        if not self.chroma_id:
            self.chroma_id = str(uuid.uuid4())

        collection = get_jobs_collection()
        vector = embed_text(self.get_embed_text())

        collection.upsert(
            ids=[self.chroma_id],
            embeddings=[vector],
            documents=[self.get_embed_text()],
            metadatas=[
                {
                    "title": self.title,
                    "company": self.company,
                    "field": self.field,
                    "description": self.description,
                    "skills": self.skills,
                }
            ],
        )

    def delete_from_chroma(self):
        """Remove this job's vector from ChromaDB."""
        if not self.chroma_id:
            return
        try:
            from matcher.vector_db import get_jobs_collection
            collection = get_jobs_collection()
            collection.delete(ids=[self.chroma_id])
        except Exception:
            pass  # Don't crash if vector is already gone

    def save(self, *args, **kwargs):
        """Override save to auto-sync with ChromaDB after DB save."""
        self.sync_to_chroma()          # embed + upsert to ChromaDB
        super().save(*args, **kwargs)  # save chroma_id to Django DB


@receiver(post_delete, sender=Job)
def remove_from_chroma_on_delete(sender, instance, **kwargs):
    """Signal: when a Job is deleted from admin, remove it from ChromaDB too."""
    instance.delete_from_chroma()
