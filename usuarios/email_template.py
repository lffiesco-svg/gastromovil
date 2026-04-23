def get_email_html(titulo, contenido_central):
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f4f4f4" style="padding:40px 0; font-family:Arial,sans-serif;">
    <tr>
        <td align="center">
        <table width="580" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="border-radius:12px; overflow:hidden;">

            <tr>
            <td bgcolor="#c0392b" style="padding:30px; text-align:center;">
                <p style="margin:0; font-size:30px;">🍽️</p>
                <h1 style="color:#ffffff; margin:8px 0 0 0; font-size:24px; font-family:Arial,sans-serif;">GastroWeb</h1>
            </td>
            </tr>

            <tr>
            <td style="padding:30px 50px 10px 50px;">
                <h2 style="color:#c0392b; margin:0; font-size:20px; font-family:Arial,sans-serif;">{titulo}</h2>
            </td>
            </tr>

            <tr>
            <td style="padding:10px 50px 30px 50px;">
                {contenido_central}
            </td>
            </tr>

            <tr>
            <td bgcolor="#f9f9f9" style="padding:20px; text-align:center; border-top:1px solid #eeeeee;">
                <p style="color:#aaaaaa; font-size:12px; margin:0; font-family:Arial,sans-serif;">
                © 2026 GastroWeb · Si no reconoces esta acción, ignora este mensaje.
                </p>
            </td>
            </tr>

        </table>
        </td>
    </tr>
    </table>
    """


def codigo_box(codigo):
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
        <td align="center" style="padding:20px 0;">
        <table cellpadding="0" cellspacing="0">
            <tr>
            <td bgcolor="#f4f4f4" style="border:2px dashed #c0392b; border-radius:10px; padding:20px 40px;">
                <span style="font-size:36px; font-weight:bold; color:#c0392b; letter-spacing:8px; font-family:Arial,sans-serif;">{codigo}</span>
            </td>
            </tr>
        </table>
        </td>
    </tr>
    </table>
    """


def parrafo(texto):
    return f'<p style="color:#555555; font-size:15px; line-height:1.7; font-family:Arial,sans-serif;">{texto}</p>'


def nota(texto):
    return f'<p style="color:#aaaaaa; font-size:13px; text-align:center; font-family:Arial,sans-serif;">{texto}</p>' 