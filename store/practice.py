# Uls.py
path('update_info', views.update_info, name='update_info')

# Update_info.html
{% extends 'base.html' %}
{% load static %}
{% block content %}

    <!-- Header-->
    <header class="bg-dark py-5" ><!--style="background-image: url('{% static 'b.webp' %}'); background-size: cover; background-position: center;"-->
        <div class="container px-4 px-lg-5 ">
            <div class="text-center text-black">
                    <h1 class="display-4 fw-bolder">Update Profile Info</h1>
                    <p class="lead fw-normal text-red-50 mb-0">Update Your Profile Info...</p>
            </div>
        </div>
    </header> 

    <br>
    <div class="  container border rounded rounded-3 border-white " >
       <div class="row">
            <div class="col-md-6 offset-md-3"> 
                <br/>
                <form method="POST" action="{% url 'update_info' %}">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <br/>

                    <button type="submit" class="btn btn-secondary">
                        Update Profile
                    </button> 
                    &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;&nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;
                    &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;
                    &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;&nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;
                    <a href="{% url 'update_password' %}">Forgot Your Password?</a>
                </form>

               
            </div>	
        </div>
    </div>
    <br/><br/>
        
{% endblock %}



# Base.html
 <!-- Logged OIn User -->
                        {% if user.is_authenticated %}
                            <!-- User Profile data -->
                            <li class="nav-item"><a class="nav-link" href="{% url 'logout' %}">Logout</a></li>
                            
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" id="navbarDropdown" href="#" 
                                role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    Profile
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                                    <li><a class="dropdown-item" href="{% url 'update_info' %}">My profile</a></li>
                                    <li><hr class="dropdown-divider" /></li>
                                    <li><a class="dropdown-item" href="{% url 'update_user'  %}">Update Info</a></li>
                                    <li><a class="dropdown-item" href="{% url 'logout'  %}">Logout</a></li>
                                    
                                </ul>
                            </li>
                            
                        </li>

                        {% else %}


# Views.py
from .models import Profile
from .forms import UpdateInfoForm

def update_info(request):
    # Is the user Logged in? Validate
    if request.user.is_validated:
        # Which user/ what user?
        current_user = Profile.objects.get(user__id= request.user.id)

        # Lets create a form
        form = UpdateInfoForm(request.POST or None, instance=current_user)

        # lets login the user and validate the form
        if form.is_valid():
            form.save()
            message
            return redirect('home')
        return render(request, 'update_info.html', {'form':form})
    else:
        message 
        return redirect('home')
         

#views.py
from .models import Profile 
class UpdateInfoForm(forms.ModelForm):
    phone = forms.CharField(label="Phone Number",  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone number'}), required=False)
    address1 = forms.CharField(label="Address 1",  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}), required=False)
    address2 = forms.CharField(label="address 2",  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}), required=False)
    city = forms.CharField(label="City",  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'city'}), required=False)
    province = forms.CharField(label="Province",  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'province'}), required=False)
    zipcode = forms.CharField(label="zipcode",  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'zipcode'}), required=False)
    country = forms.CharField(label="Country",  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'country'}), required=False)

    class Meta:
        model = Profile
        fields = ["phone", 'address1', 'address2', 'city', "city", "province", "zipcode", "country",]












# Search Funtionaluty
# Urls.py
path('search', views.search, name='search')

# search.html
{% extends 'base.html' %}
{% load static %}
{% block content %}

    <!-- Header-->
    <header class="bg-dark py-5" style="background-image: url('{% static 'we.webp' %}'); background-size: cover; background-position: center;">
        <div class="container px-4 px-lg-5 ">
            <div class="text-center text-black">
                <h1 class="display-4 fw-bolder">Search</h1>
                <p class="lead fw-normal text-red-50 mb-0">Find What You're Looking For...</p>
            </div>
        </div>
    </header> 

    <section class="py-5">
        <div class="container">
            <form method="POST" action="{% url 'search' %}">
            {% csrf_token %}
            <div class="mb-3">
                <input type="text" class="form-control" placeholder="Search For Products" name="searched">
            </div>
            <button type="submit" class="btn btn-secondary">
                Search Products
            </button>
        </form>
        {% if searched %}




        </div>
    </section>

{% endblock %}


# Add search t nav bar
# vews.py
from djnago.db.models import Q
from .models import Product

def search(request):
    # Determine if user filled the form
    if request.method == 'POST':
        searched = request.POST['searched']

        # query Product DB model for produuct
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test for Nul
        if not searched:
            messages.success()
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'serached': searched})
    else:
        return render(request, 'search.html', {})