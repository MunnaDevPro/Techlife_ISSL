from django.shortcuts import render, redirect
from .forms import ContactOrSupportForm

# def contact_or_support_view(request):
#     if request.method == 'POST':
#         form = ContactOrSupportForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # if request.user.is_authenticated:
#             #     contact.user = request.user
#             # contact.save()
#             return redirect('home')  
#     else:
#         form = ContactOrSupportForm()

#     return render(request, 'include/contact_us_page.html', {'form': form})

def contact_or_support_view(request):
    if request.method == 'POST':
        form = ContactOrSupportForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user = request.user
            contact.save()
            return redirect('homepage')

    else:
        form = ContactOrSupportForm()

    return render(request, 'include/contact_us_page.html', {'form': form})
