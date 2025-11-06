import smtplib
from email.message import EmailMessage
from typing import List
from . import purchase_service
from config.email import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_USE_TLS, EMAIL_FROM, PURCHASE_EMAILS
import html


def format_ticket_html(ticket: dict) -> str:
    """Genera un cuerpo HTML simple para el ticket"""
    lines = []
    lines.append(f"<h2>Ticket de Compra - {html.escape(ticket.get('ticket_id',''))}</h2>")
    lines.append(f"<p>Fecha: {html.escape(ticket.get('purchase_date',''))}</p>")
    lines.append(f"<p>Cliente: {html.escape(str(ticket.get('user_name','')))}</p>")
    lines.append('<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse">')
    lines.append('<thead><tr><th>Producto</th><th>Cantidad</th><th>Precio Unit.</th><th>Total</th></tr></thead>')
    lines.append('<tbody>')
    for it in ticket.get('items', []):
        pname = html.escape(str(it.get('product_name','')))
        qty = html.escape(str(it.get('quantity','')))
        unit = f"{float(it.get('unit_price',0.0)):.2f}"
        total = f"{float(it.get('total',0.0)):.2f}"
        lines.append(f"<tr><td>{pname}</td><td align=\"center\">{qty}</td><td align=\"right\">${unit}</td><td align=\"right\">${total}</td></tr>")
    lines.append('</tbody>')
    lines.append(f"<tfoot><tr><td colspan=\"3\" align=\"right\"><strong>Total</strong></td><td align=\"right\"><strong>${float(ticket.get('total_amount',0.0)):.2f}</strong></td></tr></tfoot>")
    lines.append('</table>')
    lines.append('<p>Gracias por su compra.</p>')
    return '\n'.join(lines)


def send_purchase_ticket_email(ticket: dict, recipients: List[str] = None) -> bool:
    """Enviar el ticket a los destinatarios listados. Devuelve True si el envío se intenta sin lanzar excepción.

    Si recipients es None, se buscará la variable PURCHASE_EMAILS de configuración.
    """
    if recipients is None:
        raw = PURCHASE_EMAILS or ''
        recipients = [r.strip() for r in raw.split(',') if r.strip()]

    if not recipients:
        # No hay destinatarios configurados: no hacemos nada
        return False

    # Construir mensaje
    msg = EmailMessage()
    subject = f"Ticket de Compra {ticket.get('ticket_id','')}"
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = ', '.join(recipients)

    # Plain text fallback
    plain_lines = [f"Ticket ID: {ticket.get('ticket_id','')}", f"Fecha: {ticket.get('purchase_date','')}", f"Cliente: {ticket.get('user_name','')}", '']
    for it in ticket.get('items', []):
        plain_lines.append(f"- {it.get('product_name','')} x{it.get('quantity',0)} -> ${it.get('total',0.0):.2f}")
    plain_lines.append(f"Total: ${ticket.get('total_amount',0.0):.2f}")
    plain_text = '\n'.join(plain_lines)

    html_body = format_ticket_html(ticket)

    msg.set_content(plain_text)
    msg.add_alternative(f"<html><body>{html_body}</body></html>", subtype='html')

    # Enviar vía SMTP
    try:
        if SMTP_USE_TLS:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
            server.starttls()
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)

        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)

        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        # No queremos que un fallo de correo rompa la compra; loggear y devolver False
        try:
            import logging
            logging.getLogger(__name__).exception('Error enviando email de ticket: %s', e)
        except Exception:
            pass
        return False
