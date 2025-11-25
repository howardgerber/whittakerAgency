# Slice 7: Email & Notifications

**Estimated Time:** 4-6 hours
**Dependencies:** Slices 3 (Quote System) and 4 (Claims System) must be complete
**Status:** Not started

---

## Overview

This slice implements email notifications using Brevo (formerly SendinBlue) as the email service provider. Notifications will be sent to administrators when users submit quotes or claims, and to customers when their requests are reviewed or updated.

---

## Goals

- [ ] Configure Brevo API integration
- [ ] Create email service with template support
- [ ] Implement admin notifications for new quotes
- [ ] Implement admin notifications for new claims
- [ ] Implement customer notifications for quote responses
- [ ] Implement customer notifications for claim updates
- [ ] Add email logging and error handling
- [ ] Create email templates with branding
- [ ] Test all email workflows

---

## Features to Implement

### 1. Email Service Configuration

**Brevo Setup:**
- [ ] Create Brevo account (if not already exists)
- [ ] Generate API key
- [ ] Configure sender email and verify domain
- [ ] Set up email templates in Brevo dashboard (optional)

**Environment Configuration:**
```env
BREVO_API_KEY=xkeysib-xxxxxxxxxxxxxxxxxxxxx
BREVO_SENDER_EMAIL=noreply@whittakeragency.com
BREVO_SENDER_NAME=Whittaker Agency
BREVO_ADMIN_EMAIL=kyle@whittakeragency.com
```

### 2. Backend Email Service

**File:** `backend/app/services/email_service.py`

**Functionality:**
- [ ] Send email via Brevo API
- [ ] Template rendering (plain text and HTML)
- [ ] Error handling and logging
- [ ] Email queue (optional, for reliability)
- [ ] Rate limiting compliance

**Email Types to Support:**
1. Quote request notification (to admin)
2. Claim submission notification (to admin)
3. Quote response notification (to customer)
4. Claim status update notification (to customer)
5. Contact form submission (to admin)
6. Password reset (if needed)
7. Welcome email (optional)

### 3. Email Templates

**Template Structure:**
- Clean, professional design
- Whittaker Agency branding (colors: #003DA5, #FFFFFF)
- Mobile-responsive HTML
- Plain text fallback
- Clear call-to-action buttons
- Contact information footer

**Template 1: New Quote Request (to Admin)**
```
Subject: New Quote Request - [Insurance Type]

A new quote request has been submitted:

Customer: [Name]
Email: [Email]
Phone: [Phone]
Insurance Type: [Category - Subcategory]
Submitted: [Date/Time]

Quote Details:
[Dynamic fields based on quote type]

Customer Notes:
[Notes if provided]

View in dashboard: [Link]

---
Whittaker Agency
Your Family, Your Business, Our Priority
```

**Template 2: New Claim Submission (to Admin)**
```
Subject: New Claim Submitted - [Insurance Type]

A new claim has been submitted:

Customer: [Name]
Email: [Email]
Policy Number: [Policy #]
Insurance Type: [Type]
Incident Date: [Date]
Submitted: [Date/Time]

Claim Details:
[Dynamic fields based on claim type]

Customer Description:
[Description]

View in dashboard: [Link]

---
Whittaker Agency
Your Family, Your Business, Our Priority
```

**Template 3: Quote Response (to Customer)**
```
Subject: Your Insurance Quote is Ready

Hello [Name],

Thank you for requesting a quote from Whittaker Agency. We've reviewed your request for [Insurance Type] coverage.

Quote Amount: $[Amount]/[period]
Valid Until: [Date]

[Agent response/notes]

Next Steps:
- Review your quote details: [Link to dashboard]
- Contact us with questions: (503) 555-1234
- Accept your quote online or call us to get started

We're here to help with any questions you may have.

Best regards,
Kyle Whittaker
Whittaker Agency
Your Family, Your Business, Our Priority

---
Questions? Reply to this email or call (503) 555-1234
Visit us: www.whittakeragency.com
```

**Template 4: Claim Status Update (to Customer)**
```
Subject: Update on Your Claim - [Claim ID]

Hello [Name],

Your claim has been updated.

Claim ID: [ID]
Insurance Type: [Type]
Status: [Status]
Updated: [Date/Time]

[Agent notes/update message]

View your claim details: [Link]

If you have any questions, please contact us at (503) 555-1234.

Best regards,
Whittaker Agency Team

---
Whittaker Agency
Your Family, Your Business, Our Priority
```

### 4. Integration Points

**Quote Service Integration:**
```python
# In backend/app/services/quote_service.py
# After creating quote:
EmailService.send_new_quote_notification(
    admin_email=settings.BREVO_ADMIN_EMAIL,
    quote=new_quote,
    user=user
)
```

**Claim Service Integration:**
```python
# In backend/app/services/claim_service.py
# After creating claim:
EmailService.send_new_claim_notification(
    admin_email=settings.BREVO_ADMIN_EMAIL,
    claim=new_claim,
    user=user
)
```

**Quote Update Integration:**
```python
# When admin provides quote response:
if quote.status == QuoteStatus.QUOTED:
    EmailService.send_quote_response(
        customer_email=user.email,
        quote=quote
    )
```

**Claim Update Integration:**
```python
# When admin updates claim status:
EmailService.send_claim_status_update(
    customer_email=user.email,
    claim=claim,
    update_message=agent_notes
)
```

---

## Technical Implementation

### Backend Files to Create

```
backend/app/
├── services/
│   └── email_service.py           # Main email service
├── templates/
│   └── email/
│       ├── new_quote_admin.html   # Admin quote notification
│       ├── new_quote_admin.txt    # Plain text version
│       ├── new_claim_admin.html   # Admin claim notification
│       ├── new_claim_admin.txt    # Plain text version
│       ├── quote_response.html    # Customer quote response
│       ├── quote_response.txt     # Plain text version
│       ├── claim_update.html      # Customer claim update
│       └── claim_update.txt       # Plain text version
└── core/
    └── config.py                   # Already has email config
```

### Email Service Implementation

```python
# backend/app/services/email_service.py
import httpx
from app.core.config import settings
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails via Brevo API"""

    BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

    @staticmethod
    async def send_email(
        to_email: str,
        to_name: str,
        subject: str,
        html_content: str,
        text_content: str
    ) -> bool:
        """
        Send email via Brevo API

        Args:
            to_email: Recipient email address
            to_name: Recipient name
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            headers = {
                "accept": "application/json",
                "api-key": settings.BREVO_API_KEY,
                "content-type": "application/json"
            }

            payload = {
                "sender": {
                    "name": "Whittaker Agency",
                    "email": settings.BREVO_SENDER_EMAIL
                },
                "to": [
                    {
                        "email": to_email,
                        "name": to_name
                    }
                ],
                "subject": subject,
                "htmlContent": html_content,
                "textContent": text_content
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.BREVO_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=10.0
                )

            if response.status_code == 201:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False

    @staticmethod
    def send_new_quote_notification(admin_email: str, quote, user):
        """Send notification to admin when new quote is submitted"""
        # Implementation details
        pass

    @staticmethod
    def send_new_claim_notification(admin_email: str, claim, user):
        """Send notification to admin when new claim is submitted"""
        # Implementation details
        pass

    @staticmethod
    def send_quote_response(customer_email: str, quote):
        """Send quote response to customer"""
        # Implementation details
        pass

    @staticmethod
    def send_claim_status_update(customer_email: str, claim, update_message: str):
        """Send claim status update to customer"""
        # Implementation details
        pass
```

### Dependencies to Add

```txt
# Add to backend/requirements.txt
httpx==0.25.2  # Already exists for async HTTP requests
jinja2==3.1.2  # For template rendering
```

---

## Email Template Variables

### Quote Notification Variables
- `customer_name`: User's full name
- `customer_email`: User's email
- `customer_phone`: User's phone (if provided)
- `insurance_category`: Category (Vehicle, Property, etc.)
- `insurance_subcategory`: Subcategory (Auto, Homeowners, etc.)
- `quote_id`: Quote request ID
- `submitted_date`: Submission timestamp
- `quote_details`: Dynamic fields as key-value pairs
- `customer_notes`: Additional notes from customer
- `dashboard_link`: Link to view in admin dashboard

### Claim Notification Variables
- `customer_name`: User's full name
- `customer_email`: User's email
- `policy_number`: Policy number (if provided)
- `insurance_type`: Type of insurance
- `incident_date`: Date of incident
- `claim_id`: Claim ID
- `submitted_date`: Submission timestamp
- `claim_description`: Customer's description
- `dashboard_link`: Link to view in admin dashboard

### Quote Response Variables
- `customer_name`: User's first name
- `insurance_type`: Full insurance type
- `quote_amount`: Quote amount with currency
- `quote_period`: Billing period (month, year, etc.)
- `valid_until`: Quote expiration date
- `agent_response`: Agent's notes/response
- `quote_link`: Link to view quote in customer dashboard

### Claim Update Variables
- `customer_name`: User's first name
- `claim_id`: Claim ID
- `insurance_type`: Type of insurance
- `status`: Current claim status
- `updated_date`: Update timestamp
- `update_message`: Agent's update message
- `claim_link`: Link to view claim in customer dashboard

---

## Testing Checklist

### Email Service Testing
- [ ] Send test email via Brevo API
- [ ] Verify HTML rendering
- [ ] Verify plain text fallback
- [ ] Test error handling for invalid API key
- [ ] Test error handling for invalid email address
- [ ] Verify email logging

### Integration Testing
- [ ] New quote triggers admin notification
- [ ] New claim triggers admin notification
- [ ] Quote response triggers customer notification
- [ ] Claim update triggers customer notification
- [ ] All template variables render correctly
- [ ] Links in emails are correct and working

### Template Testing
- [ ] All templates render on desktop email clients
- [ ] All templates render on mobile email clients
- [ ] All templates render on webmail (Gmail, Outlook, Yahoo)
- [ ] Links are clickable
- [ ] Branding is consistent
- [ ] Plain text versions are readable

### Error Handling
- [ ] Failed email sends are logged
- [ ] System continues working if email fails
- [ ] Retry logic for temporary failures (optional)
- [ ] Admin notified of email delivery issues (optional)

---

## Success Criteria

- Brevo API integration working correctly
- Admin receives email notifications for new quotes
- Admin receives email notifications for new claims
- Customers receive email when quote is ready
- Customers receive email when claim is updated
- All emails render correctly on major email clients
- Email failures logged but don't break main functionality
- Templates are branded and professional
- All links in emails work correctly
- No console errors related to email sending

---

## Security Considerations

- [ ] API key stored securely in environment variables
- [ ] Never expose API key in client-side code
- [ ] Validate email addresses before sending
- [ ] Rate limiting to prevent abuse
- [ ] Sanitize data before including in emails
- [ ] Use HTTPS for all API calls
- [ ] Don't log sensitive customer information
- [ ] Include unsubscribe link (if doing marketing emails)

---

## Future Enhancements (Not in this slice)

- Email preferences (customer can opt out of certain emails)
- SMS notifications as alternative
- Push notifications for mobile app
- Email templates in Brevo dashboard (instead of code)
- Email scheduling (send at optimal times)
- Email analytics and open rates
- Bulk email sending for newsletters
- Automated reminder emails

---

## Estimated Breakdown

**Brevo Setup & Configuration:** 30 minutes
- Create account
- Generate API key
- Configure sender domain

**Email Service Implementation:** 2-3 hours
- Create email service class
- Implement send methods
- Add error handling
- Add logging

**Email Templates:** 2-3 hours
- Design HTML templates
- Create plain text versions
- Test rendering
- Ensure mobile responsiveness

**Integration with Existing Services:** 1 hour
- Add email calls to quote service
- Add email calls to claim service
- Test integration

**Testing & Polish:** 1 hour
- Test all email workflows
- Verify template rendering
- Fix any issues

**Total:** 4-6 hours

---

## Notes for Implementation

- Start with one email type (e.g., new quote notification) and test thoroughly
- Use Jinja2 for template rendering
- Keep templates simple and professional
- Test on multiple email clients (Gmail, Outlook, Apple Mail)
- Make sure emails work in dark mode
- Consider using inline CSS for better email client compatibility
- Log all email attempts for debugging
- Make email sending async to avoid blocking requests
- Consider using a retry mechanism for failed sends

---

**Document Version:** 1.0
**Created:** 2025-11-04
**Last Updated:** 2025-11-04
