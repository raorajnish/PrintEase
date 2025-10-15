# PrintEase - Print Shop Management Platform

PrintEase is a Django-based web application that connects users with print shops for document printing services. The platform facilitates seamless interaction between customers and print shop owners, enabling users to upload documents, specify printing requirements, and get instant pricing estimates.

## 🚀 Features

### For Users
- **Browse Print Shops**: View available print shops in the area
- **Document Upload**: Upload multiple documents (PDF, DOCX, etc.) for printing
- **Customizable Printing Options**:
  - Black & White or Color printing
  - Single or Double-sided printing
  - Custom page selection
  - Multiple copies
- **Instant Price Calculation**: Real-time pricing based on shop rates
- **User Registration & Authentication**: Secure login/logout system

### For Print Shop Owners
- **Shop Profile Management**: Complete shop details with location and contact information
- **Pricing Configuration**: Set rates for black & white and color printing
- **Operating Hours**: Define business hours
- **Email Notifications**: Receive confirmation emails for profile updates
- **Dashboard**: Manage shop information and view orders

## 🛠️ Technology Stack

- **Backend**: Django 5.1.6
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Remix Icons
- **File Processing**: PyPDF2, python-docx
- **Email**: SMTP (Gmail)

## 📁 Project Structure

```
printease1/
├── pe/                          # Main Django project
│   ├── app/                     # Core application
│   │   ├── models.py           # Shop details and business logic
│   │   ├── views.py            # Main application views
│   │   ├── forms.py            # Shop details form
│   │   ├── templates/          # HTML templates
│   │   └── static/             # CSS, JS, Images
│   ├── users/                  # User authentication app
│   │   ├── models.py          # Custom user model
│   │   ├── views.py           # Authentication views
│   │   └── templates/         # User templates
│   ├── pe/                    # Django settings
│   │   ├── settings.py        # Project configuration
│   │   └── urls.py           # Main URL routing
│   └── manage.py              # Django management
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🗄️ Database Models

### User Model (Custom)
- `is_admin`: Admin privileges
- `is_user`: Regular user privileges  
- `is_shop`: Print shop owner privileges

### ShopDetails Model
- **Basic Info**: Shop name, owner name, contact number
- **Location**: Area, city, state, pincode (Indian states supported)
- **Business Details**: GSTIN, operating hours
- **Pricing**: Black & white and color print rates
- **Status**: Details completion tracking

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd printease1
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   cd pe
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`

## 📧 Email Configuration

The application uses Gmail SMTP for sending emails. Update the following settings in `pe/pe/settings.py`:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

**Note**: Use Gmail App Password, not your regular password.

## 🎨 Key Features Explained

### User Authentication System
- Custom user model with role-based access
- Separate registration for users and shop owners
- Secure login/logout functionality

### Print Shop Management
- Shop owners can register and provide detailed information
- Location-based shop discovery
- Pricing transparency with instant calculations

### Document Processing
- Support for multiple file formats (PDF, DOCX)
- Page counting and custom page selection
- File upload with secure storage

### Real-time Pricing
- Dynamic price calculation based on:
  - Number of pages
  - Print type (B/W or Color)
  - Number of copies
  - Shop-specific rates
- **Note**: Payment integration will be added in future updates

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root for sensitive data:

```env
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Database Configuration
The project uses SQLite by default. For production, consider PostgreSQL or MySQL.

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📱 Responsive Design

The application features a responsive design that works on:
- Desktop computers
- Tablets
- Mobile devices

## 🔒 Security Features

- CSRF protection enabled
- Secure file upload handling
- Input validation and sanitization
- Role-based access control

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up proper email backend
4. Configure static file serving
5. Set up HTTPS
6. Update `ALLOWED_HOSTS`

### Recommended Deployment Options
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with Nginx and Gunicorn
- **AWS**: Elastic Beanstalk or EC2

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Developer**: [Your Name]
- **Project**: PrintEase
- **Version**: 1.0.0

## 📞 Support

For support and questions:
- Email: pe.printease@gmail.com
- Create an issue in the repository

## 🔄 Future Enhancements

- [ ] Payment gateway integration (Razorpay)
- [ ] Order tracking system
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] API for third-party integrations

---

**PrintEase** - Making printing services accessible and convenient for everyone! 🖨️✨
