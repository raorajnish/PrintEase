# PrintEase

PrintEase is an online document printing service where users can upload multiple PDF and DOCX files, customize their print preferences, and proceed to checkout. The system automatically calculates the total price based on the number of pages and print type (Black & White or Color). Orders and payments are managed within the platform.

## Features

- **User Authentication:** Users can sign up, log in, and manage their orders.
- **Upload Multiple Documents:** Accepts PDFs and DOCX files.
- **Automatic Page Count Detection:** Extracts page numbers from the uploaded file.
- **Custom Page Selection:** Validates and allows users to print specific pages.
- **Dynamic Price Calculation:** Based on print type (B&W or Color) and total pages.
- **Order Management:** Associates print files with orders linked to users.
- **Payment Integration:** Uses Razorpay for payments.
- **Admin Panel:** Manage orders and update statuses (Pending, Confirmed, Ready to Take, Cancelled).

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/raorajnish/PrintEase.git
   cd PrintEase
   ```
2. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create Superuser (Optional - For Admin Access):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run Development Server:**
   ```bash
   python manage.py runserver
   ```

## Dependencies

The required dependencies are included in `requirements.txt`. Key packages used:
- Django
- Pillow (for handling document uploads)
- PyPDF2 (for extracting page count from PDFs)
- python-docx (for extracting page count from DOCX files)
- Razorpay (for payment integration)

## Usage

- **Upload Print Files:** Users can upload PDFs and DOCX files, select print options, and proceed to checkout.
- **Checkout and Payment:** After verifying order details, users can complete payment using Razorpay.
- **Order Management:** Users can view their past orders and track their status.

## API Endpoints

| Method | Endpoint         | Description |
|--------|----------------|-------------|
| GET    | `/upload/`      | Upload print files page |
| POST   | `/upload/`      | Submit multiple files |
| GET    | `/checkout/`    | Checkout page with order details |
| POST   | `/payment/`     | Handle payment processing |
| GET    | `/orders/`      | View past orders |

## Troubleshooting

- **Page count not detected?** Ensure that the file format is correct (PDF or DOCX only).
- **Payment issues?** Check Razorpay settings in `settings.py`.
- **Server not starting?** Verify dependencies are installed (`pip install -r requirements.txt`).

## Future Enhancements

- Allow users to reorder past print files.
- Support additional document formats (e.g., PPT, ODT).
- Implement real-time order tracking notifications.

## License

This project is open-source under the MIT License.

## Contributing

Pull requests are welcome! Open an issue for feature requests or bug reports.

---

Happy printing with PrintEase! 🖨️🚀
