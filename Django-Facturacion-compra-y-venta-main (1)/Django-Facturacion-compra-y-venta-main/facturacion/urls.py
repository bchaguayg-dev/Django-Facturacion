from django.urls import path               # path() une una dirección con una vista
from . import views                        # Las vistas de ESTA app (facturacion/views.py)

app_name = "facturacion"                   # "Apellido" de las URLs de esta app. En templates: 'facturacion:marca_lista'

urlpatterns = [
        # ---------- MARCAS: clases (VBC) · Tarea 1 ----------
    path("marcas/", views.MarcaListView.as_view(), name="marca_lista"),                          # .as_view(): obligatorio en clases
    path("marcas/crear/", views.MarcaCreateView.as_view(), name="marca_crear"),
    path("marcas/editar/<int:pk>/", views.MarcaUpdateView.as_view(), name="marca_editar"),       # pk → get_object()
    path("marcas/eliminar/<int:pk>/", views.MarcaDeleteView.as_view(), name="marca_eliminar"),
    
    # ---------- PRODUCTOS: clases (VBC) ----------
    path("productos/", views.ProductoListView.as_view(), name="producto_lista"),   # .as_view(): obligatorio en clases
    path("productos/crear/", views.ProductoCreateView.as_view(), name="producto_crear"),
    path("productos/editar/<int:pk>/", views.ProductoUpdateView.as_view(), name="producto_editar"),   # pk → get_object()
    path("productos/<int:pk>/", views.ProductoDetailView.as_view(), name="producto_detalle"),
    path("productos/eliminar/<int:pk>/", views.ProductoDeleteView.as_view(), name="producto_eliminar"),


    # ---------- CATEGORÍAS: clases (VBC) · Tarea 2 ----------
    path("categorias/", views.CategoriaListView.as_view(), name="categoria_lista"),
    path("categorias/crear/", views.CategoriaCreateView.as_view(), name="categoria_crear"),
    path("categorias/editar/<int:pk>/", views.CategoriaUpdateView.as_view(), name="categoria_editar"),
    path("categorias/eliminar/<int:pk>/", views.CategoriaDeleteView.as_view(), name="categoria_eliminar"),
    # ---------- CLIENTES: clases (VBC) · Tarea 3 ----------
    path("clientes/", views.ClienteListView.as_view(), name="cliente_lista"),
    path("clientes/crear/", views.ClienteCreateView.as_view(), name="cliente_crear"),
    path("clientes/<int:pk>/", views.ClienteDetailView.as_view(), name="cliente_detalle"),
    path("clientes/editar/<int:pk>/", views.ClienteUpdateView.as_view(), name="cliente_editar"),
    path("clientes/eliminar/<int:pk>/", views.ClienteDeleteView.as_view(), name="cliente_eliminar"),

    # ---------- PROVEEDORES: clases (VBC) · Tarea 4 ----------
    path("proveedores/", views.ProveedorListView.as_view(), name="proveedor_lista"),
    path("proveedores/crear/", views.ProveedorCreateView.as_view(), name="proveedor_crear"),
    path("proveedores/editar/<int:pk>/", views.ProveedorUpdateView.as_view(), name="proveedor_editar"),
    path("proveedores/eliminar/<int:pk>/", views.ProveedorDeleteView.as_view(), name="proveedor_eliminar"),
    # ---------- RETO · MI PERFIL ----------
    path("mi-perfil/", views.MiPerfilView.as_view(), name="mi_perfil"),   # sin <int:pk>: get_object() lo resuelve
]