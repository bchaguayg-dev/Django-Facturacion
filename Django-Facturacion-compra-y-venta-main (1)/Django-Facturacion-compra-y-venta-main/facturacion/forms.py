from django import forms

from .models import Categoria, Cliente, Marca, Producto, Proveedor  ,Perfil  ,Venta              # El modelo del que sale el formulario


class MarcaForm(forms.ModelForm):                # ModelForm: formulario construido desde un modelo

    class Meta:                                  # Configuración del formulario
        model = Marca                            # ¿De qué modelo sale? De Marca
        fields = ["nombre", "pais_origen", "activo"]   # ¿Qué campos muestra y en qué orden?
        labels = {                               # Cambia el texto de la etiqueta de un campo
            "nombre": "Nombre de la marca",
        }
        widgets = {                              # widgets: CÓMO se dibuja cada campo en HTML
            # TextInput = <input type="text">. attrs agrega atributos HTML: aquí la clase de Bootstrap
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Samsung"}),
            "pais_origen": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Corea del Sur"}),
            # CheckboxInput = <input type="checkbox">. form-check-input es la clase de Bootstrap para casillas
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
   
    def clean_nombre(self):                      # Validación propia del campo "nombre" (clean_ + nombre del campo)
        nombre = self.cleaned_data["nombre"].strip()   # cleaned_data: los datos ya revisados. strip quita espacios
        if len(nombre) < 2:                      # Si tiene menos de 2 letras...
            raise forms.ValidationError("El nombre debe tener al menos 2 letras.")  # ...error en rojo bajo el campo
        return nombre.title()  
    
                 # Si está bien, lo devolvemos con la Primera Letra Mayúscula """



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # user, fecha_creacion y fecha_modificacion NO van: los llena el sistema
        fields = ["nombre", "descripcion", "marca", "categorias", "precio", "stock", "imagen", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Galaxy A55"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "marca": forms.Select(attrs={"class": "form-select"}),                         # 1:N → una opción
            "categorias": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),  # N:M → varias
            "precio": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            # ClearableFileInput = <input type="file"> + casilla "Limpiar" para quitar la foto actual
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["marca"].queryset = Marca.objects.filter(activo=True)   # solo marcas activas
        self.fields["marca"].empty_label = "— Elige una marca —"

    def clean_precio(self):
        precio = self.cleaned_data["precio"]
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que 0.")
        return precio




# =====================================================================
# TAREA 2 · CATEGORÍA (copia de MarcaForm + descripción)
# =====================================================================
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion", "activo"]     # user y fechas NO van: los llena el sistema
        labels = {"nombre": "Nombre de la categoría"}
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Lácteos"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),   # Textarea: caja de varias líneas
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_nombre(self):                              # igual que en MarcaForm
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 letras.")
        return nombre[0].upper() + nombre[1:]            # solo la primera letra en mayúscula


# =====================================================================
# TAREA 3 · CLIENTE (con clean_cedula)
# =====================================================================
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["cedula", "nombres", "apellidos", "email", "telefono", "direccion"]
        widgets = {
            "cedula": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 0912345678"}),
            "nombres": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Ana María"}),
            "apellidos": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Pérez López"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ej: ana@correo.com"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 0991234567"}),
            "direccion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Av. 9 de Octubre"}),
        }

    def clean_cedula(self):                              # base: clean_precio de ProductoForm
        cedula = self.cleaned_data["cedula"].strip()
        if len(cedula) != 10:                            # 1. exactamente 10 caracteres
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos.")
        if not cedula.isdigit():                         # 2. isdigit(): True solo si TODOS son números
            raise forms.ValidationError("La cédula debe tener solo números.")
        return cedula                                    # que no se repita lo revisa unique=True del modelo



# =====================================================================
# TAREA 4 · PROVEEDOR (con logo y clean_ruc) · base: ClienteForm + la imagen de ProductoForm
# =====================================================================
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["ruc", "nombre", "apellido", "email", "contacto", "logo"]
        widgets = {
            "ruc": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 0912345678001"}),
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Carlos"}),
            "apellido": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Mendoza"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ej: ventas@proveedor.com"}),
            "contacto": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 0991234567"}),
            # La MISMA línea de "imagen" en ProductoForm, pero aquí el campo se llama logo
            "logo": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
        }

    def clean_ruc(self):                                 # base: clean_cedula
        ruc = self.cleaned_data["ruc"].strip()
        if len(ruc) != 13:                               # 1. exactamente 13 caracteres
            raise forms.ValidationError("El RUC debe tener exactamente 13 dígitos.")
        if not ruc.isdigit():                            # 2. solo números
            raise forms.ValidationError("El RUC debe tener solo números.")
        if not ruc.endswith("001"):                      # 3. endswith(): ¿termina en "001"?
            raise forms.ValidationError("El RUC debe terminar en 001.")
        return ruc                                       # que no se repita lo revisa unique=True


# =====================================================================
# RETO · MI PERFIL (1:1 con User)
# =====================================================================
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["cedula", "telefono", "cargo"]         # SIN usuario: siempre es request.user (lo pone la vista)
        widgets = {
            "cedula": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 0912345678"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 0991234567"}),
            "cargo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Vendedor"}),
        }







# =====================================================================
# VENTA: cabecera (maestro)
# =====================================================================
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ["cliente", "fecha_hora", "tipo_pago"]   # subtotal, iva y total los calcula el sistema
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-select"}),
            # type="datetime-local" → el navegador muestra un calendario con hora
            "fecha_hora": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"},
                                              format="%Y-%m-%dT%H:%M"),
            "tipo_pago": forms.Select(attrs={"class": "form-select"}),   # las opciones salen de TipoPago
        }