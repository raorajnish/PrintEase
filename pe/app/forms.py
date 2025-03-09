from django import forms
from .models import ShopDetails

class ShopDetailsForm(forms.ModelForm):
    class Meta:
        model = ShopDetails
        fields = ['shop_name', 'owner_name', 'area', 'city', 'state', 'pincode', 'contact_number', 'gstin', 'start_time', 'end_time', 'bw_price', 'color_price']
        widgets = {
            'shop_name': forms.TextInput(attrs={'placeholder': 'Enter Shop Name', 'class': 'form-control'}),
            'owner_name': forms.TextInput(attrs={'placeholder': 'Enter Owner Name', 'class': 'form-control'}),
            'area': forms.TextInput(attrs={'placeholder': 'Enter Area Name', 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter City Name', 'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Enter Pincode', 'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Enter Contact Number', 'class': 'form-control'}),
            'gstin': forms.TextInput(attrs={'placeholder': 'Enter GSTIN (if applicable)', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'placeholder': 'Start Time (HH:MM)', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'placeholder': 'End Time (HH:MM)', 'class': 'form-control'}),
            'bw_price': forms.NumberInput(attrs={'placeholder': 'Enter B/W Print Price in INR', 'class': 'form-control'}),
            'color_price': forms.NumberInput(attrs={'placeholder': 'Enter Color Print Price in INR', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        gstin = cleaned_data.get('gstin')
        bw_price = cleaned_data.get('bw_price')
        color_price = cleaned_data.get('color_price')

        # Ensure all address fields are filled
        area = cleaned_data.get('area')
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        pincode = cleaned_data.get('pincode')

        if not area or not city or not state or not pincode:
            raise forms.ValidationError("All address fields (Area, City, State, Pincode) are required.")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        if gstin:
            if len(gstin) != 15:
                raise forms.ValidationError("GSTIN must be exactly 15 characters.")
            if not gstin.isalnum():
                raise forms.ValidationError("GSTIN must contain only letters and numbers.")

        if bw_price is not None and bw_price < 0:
            raise forms.ValidationError("Black & White price must be a positive number.")

        if color_price is not None and color_price < 0:
            raise forms.ValidationError("Color print price must be a positive number.")

        return cleaned_data