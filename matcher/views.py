"""
matcher/views.py
----------------
Views for the Resume-Job Matcher application.

Views:
- index       : GET shows the search form; POST processes the input
- results     : Displays top 5 matching jobs
- how_it_works: Explains vector embeddings and semantic search
"""

import pdfplumber
from django.shortcuts import render, redirect
from django.contrib import messages
from .vector_db import search_jobs, get_job_count


def index(request):
    """
    Home page view.
    GET  → render the input form
    POST → extract text from PDF or use typed text, then search
    """
    job_count = get_job_count()

    if request.method == "POST":
        query_text = ""

        # User uploaded a PDF resume
        uploaded_file = request.FILES.get("resume_pdf")
        if uploaded_file and uploaded_file.name.endswith(".pdf"):
            # Server-side 5 MB size limit
            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(
                    request,
                    "File is too large. Please upload a PDF under 5 MB.",
                )
                return render(request, "matcher/index.html", {"job_count": job_count})
            try:
                with pdfplumber.open(uploaded_file) as pdf:
                    pages_text = []
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            pages_text.append(text)
                    query_text = "\n".join(pages_text)
            except Exception as e:
                messages.error(request, f"Could not read PDF: {str(e)}")
                return render(request, "matcher/index.html", {"job_count": job_count})

        # User typed their skills/experience
        if not query_text:
            query_text = request.POST.get("skills_text", "").strip()

        if not query_text:
            messages.error(
                request,
                "Please either upload a PDF resume or type your skills/experience.",
            )
            return render(request, "matcher/index.html", {"job_count": job_count})

        if len(query_text) < 20:
            messages.error(
                request,
                "Please provide more detail (at least a sentence) for better results.",
            )
            return render(request, "matcher/index.html", {"job_count": job_count})

        # Store in session and redirect to results
        request.session["query_text"] = query_text[:3000]  # limit for session storage
        return redirect("matcher:results")

    return render(request, "matcher/index.html", {"job_count": job_count})


def results(request):
    """
    Results page - retrieves top 5 jobs from ChromaDB and displays them.
    """
    query_text = request.session.get("query_text", "")

    if not query_text:
        return redirect("matcher:index")

    try:
        matched_jobs = search_jobs(query_text, n_results=5)
        # Pre-split skills into a list for template iteration
        for job in matched_jobs:
            job["skills_list"] = [s.strip() for s in job["skills"].split(",")]
    except Exception as e:
        messages.error(request, f"Search error: {str(e)}")
        return redirect("matcher:index")

    # Truncate query for display
    display_query = query_text[:200] + "..." if len(query_text) > 200 else query_text

    context = {
        "jobs": matched_jobs,
        "query_preview": display_query,
        "total_results": len(matched_jobs),
    }
    return render(request, "matcher/results.html", context)


def how_it_works(request):
    """
    Informational page explaining vector embeddings and semantic search.
    """
    return render(request, "matcher/how_it_works.html")
