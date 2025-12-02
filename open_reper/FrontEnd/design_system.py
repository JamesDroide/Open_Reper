"""
Sistema de Diseño Completo - OpenReper
Componentes base reutilizables con responsividad integrada
"""

import reflex as rx
from open_reper.FrontEnd.constants import *


# ============================================
# COLORES SEMÁNTICOS
# ============================================

COLORS = {
    "primary": BLUE_DARK,
    "primary_hover": BLUE_HOVER,
    "secondary": ORANGE,
    "secondary_hover": ORANGE_HOVER,
    "success": COLOR_SUCCESS,
    "error": COLOR_ERROR,
    "warning": COLOR_WARNING,
    "info": COLOR_INFO,
    "white": WHITE,
    "gray": GRAY,
}


# ============================================
# TIPOGRAFÍA
# ============================================

TYPOGRAPHY = {
    "h1": FONT_XXL,
    "h2": FONT_XL,
    "h3": FONT_LG,
    "h4": FONT_MD,
    "body": FONT_SM,
    "small": FONT_XS,
    "tiny": FONT_XXS,
}


# ============================================
# COMPONENTES BASE
# ============================================

def responsive_text(
    content: str,
    variant: str = "body",
    color: str = WHITE,
    weight: str = FONT_WEIGHT_NORMAL,
    align: str = "left",
    **kwargs
):
    """
    Texto responsivo con variantes predefinidas

    Args:
        content: Texto a mostrar
        variant: Variante de tipografía (h1, h2, h3, body, small, tiny)
        color: Color del texto
        weight: Peso de la fuente
        align: Alineación del texto
    """
    font_size = TYPOGRAPHY.get(variant, TYPOGRAPHY["body"])

    return rx.text(
        content,
        font_size=font_size,
        color=color,
        font_weight=weight,
        text_align=align,
        font_family=FONT_FAMILY,
        **kwargs
    )


def responsive_heading(
    content: str,
    level: int = 1,
    color: str = WHITE,
    align: str = "left",
    **kwargs
):
    """
    Heading responsivo con niveles H1-H4

    Args:
        content: Texto del heading
        level: Nivel de heading (1-4)
        color: Color del texto
        align: Alineación
    """
    variants = {1: "h1", 2: "h2", 3: "h3", 4: "h4"}
    variant = variants.get(level, "h2")
    font_size = TYPOGRAPHY[variant]

    return rx.heading(
        content,
        font_size=font_size,
        color=color,
        text_align=align,
        font_family=FONT_FAMILY,
        as_=f"h{level}",
        **kwargs
    )


def responsive_button(
    text: str,
    on_click=None,
    variant: str = "primary",
    size: str = "md",
    disabled: bool = False,
    full_width: bool = False,
    **kwargs
):
    """
    Botón responsivo con variantes de estilo

    Args:
        text: Texto del botón
        on_click: Función al hacer click
        variant: Variante de color (primary, secondary, success, error)
        size: Tamaño (sm, md, lg)
        disabled: Si está deshabilitado
        full_width: Si ocupa todo el ancho
    """
    # Colores según variante
    colors_map = {
        "primary": (COLORS["primary"], COLORS["primary_hover"]),
        "secondary": (COLORS["secondary"], COLORS["secondary_hover"]),
        "success": (COLOR_SUCCESS, GREEN_HOVER),
        "error": (COLOR_ERROR, "#C62828"),
    }

    bg_color, hover_color = colors_map.get(variant, colors_map["primary"])

    # Tamaños
    sizes_map = {
        "sm": (FONT_XS, PADDING_SM, SIZE_BUTTON_SM),
        "md": (FONT_SM, PADDING_MD, SIZE_BUTTON_MD),
        "lg": (FONT_MD, PADDING_LG, SIZE_BUTTON_LG),
    }

    font_size, padding, height = sizes_map.get(size, sizes_map["md"])

    return rx.button(
        text,
        on_click=on_click,
        bg=bg_color,
        color=WHITE,
        font_size=font_size,
        padding=padding,
        height=height,
        border_radius=RADIUS_MD,
        cursor="pointer" if not disabled else "not-allowed",
        opacity="0.6" if disabled else "1",
        disabled=disabled,
        width="100%" if full_width else "auto",
        _hover={
            "bg": hover_color if not disabled else bg_color,
            "transform": "translateY(-2px)" if not disabled else "none",
            "box_shadow": SHADOW_MD if not disabled else SHADOW_NONE
        },
        transition=f"all {TRANSITION_NORMAL[1]} {EASE_IN_OUT}",
        font_family=FONT_FAMILY,
        **kwargs
    )


def responsive_input(
    placeholder: str = "",
    value=None,
    on_change=None,
    type: str = "text",
    disabled: bool = False,
    **kwargs
):
    """
    Input responsivo con estilos consistentes

    Args:
        placeholder: Texto placeholder
        value: Valor del input
        on_change: Función al cambiar
        type: Tipo de input
        disabled: Si está deshabilitado
    """
    return rx.input(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        type=type,
        disabled=disabled,
        width="100%",
        height=HEIGHT_INPUT,
        padding=PADDING_SM,
        font_size=FONT_SM,
        border_radius=RADIUS_MD,
        border=f"2px solid {GRAY}",
        bg=WHITE,
        color="#000000",
        _focus={
            "border_color": COLORS["primary"],
            "box_shadow": SHADOW_PRIMARY,
            "outline": "none"
        },
        _disabled={
            "bg": "#F5F5F5",
            "cursor": "not-allowed"
        },
        transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}",
        **kwargs
    )


def responsive_textarea(
    placeholder: str = "",
    value=None,
    on_change=None,
    disabled: bool = False,
    **kwargs
):
    """
    Textarea responsivo con estilos consistentes

    Args:
        placeholder: Texto placeholder
        value: Valor del textarea
        on_change: Función al cambiar
        disabled: Si está deshabilitado
    """
    return rx.text_area(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        disabled=disabled,
        width="100%",
        height=HEIGHT_TEXTAREA,
        padding=PADDING_SM,
        font_size=FONT_SM,
        border_radius=RADIUS_MD,
        border=f"2px solid {GRAY}",
        bg=WHITE,
        color="#000000",
        resize="vertical",
        _focus={
            "border_color": COLORS["primary"],
            "box_shadow": SHADOW_PRIMARY,
            "outline": "none"
        },
        _disabled={
            "bg": "#F5F5F5",
            "cursor": "not-allowed"
        },
        transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}",
        font_family=FONT_FAMILY_MONO,
        **kwargs
    )


def responsive_card(
    content,
    padding: str = "md",
    shadow: str = "md",
    **kwargs
):
    """
    Card contenedor responsivo

    Args:
        content: Contenido de la card
        padding: Tamaño de padding (sm, md, lg)
        shadow: Tamaño de sombra (sm, md, lg, xl)
    """
    padding_map = {
        "sm": PADDING_SM,
        "md": PADDING_MD,
        "lg": PADDING_LG,
        "xl": PADDING_XL
    }

    shadow_map = {
        "none": SHADOW_NONE,
        "sm": SHADOW_SM,
        "md": SHADOW_MD,
        "lg": SHADOW_LG,
        "xl": SHADOW_XL,
        "xxl": SHADOW_XXL
    }

    return rx.box(
        content,
        padding=padding_map.get(padding, PADDING_MD),
        border_radius=RADIUS_LG,
        bg=BLUE_DARK,
        box_shadow=shadow_map.get(shadow, SHADOW_MD),
        width="100%",
        transition=f"all {TRANSITION_NORMAL[1]} {EASE_IN_OUT}",
        _hover={
            "box_shadow": shadow_map.get("lg", SHADOW_LG),
            "transform": "translateY(-2px)"
        },
        **kwargs
    )


def centered_container(
    content,
    max_width: str = MAX_WIDTH_LG,
    padding_x: list = None,
    **kwargs
):
    """
    Contenedor centrado responsivo

    Args:
        content: Contenido a centrar
        max_width: Ancho máximo del contenedor
        padding_x: Padding horizontal [mobile, tablet, desktop]
    """
    if padding_x is None:
        padding_x = PADDING_MD

    return rx.center(
        rx.box(
            content,
            width="100%",
            max_width=max_width,
            padding_x=padding_x,
        ),
        width="100%",
        **kwargs
    )


def responsive_grid(
    items: list,
    columns: list = None,
    gap: list = None,
    **kwargs
):
    """
    Grid responsivo que se adapta automáticamente

    Args:
        items: Lista de elementos a mostrar en el grid
        columns: Configuración de columnas [mobile, tablet, desktop]
        gap: Espacio entre items
    """
    if columns is None:
        columns = ["1fr", "repeat(2, 1fr)", "repeat(3, 1fr)"]
    if gap is None:
        gap = SPACING_MD

    return rx.flex(
        *items,
        display="grid",
        grid_template_columns=columns,
        gap=gap,
        width="100%",
        **kwargs
    )


def responsive_stack(
    items: list,
    direction: str = "vertical",
    spacing: list = None,
    align: str = "start",
    **kwargs
):
    """
    Stack responsivo (vertical u horizontal)

    Args:
        items: Lista de elementos
        direction: Dirección (vertical, horizontal)
        spacing: Espacio entre items
        align: Alineación de items
    """
    if spacing is None:
        spacing = SPACING_SM

    if direction == "vertical":
        return rx.vstack(
            *items,
            spacing=spacing[1] if isinstance(spacing, list) else spacing,
            align_items=align,
            width="100%",
            **kwargs
        )
    else:
        return rx.hstack(
            *items,
            spacing=spacing[1] if isinstance(spacing, list) else spacing,
            align_items=align,
            width="100%",
            **kwargs
        )


# ============================================
# COMPONENTES DE LAYOUT
# ============================================

def page_layout(content, header=None, footer=None):
    """
    Layout de página completo con header y footer opcionales

    Args:
        content: Contenido principal
        header: Header de la página (opcional)
        footer: Footer de la página (opcional)
    """
    elements = []

    if header:
        elements.append(header)

    elements.append(
        rx.box(
            content,
            flex="1",
            width="100%",
            overflow_y="auto"
        )
    )

    if footer:
        elements.append(footer)

    return rx.flex(
        *elements,
        flex_direction="column",
        min_height="100vh",
        width="100%",
        bg=BLUE_DARK
    )


def section_container(
    content,
    title: str = None,
    subtitle: str = None,
    **kwargs
):
    """
    Contenedor de sección con título y subtítulo opcionales

    Args:
        content: Contenido de la sección
        title: Título de la sección
        subtitle: Subtítulo de la sección
    """
    elements = []

    if title:
        elements.append(
            responsive_heading(title, level=2, align="center")
        )

    if subtitle:
        elements.append(
            responsive_text(subtitle, variant="body", color=GRAY, align="center")
        )

    elements.append(content)

    return centered_container(
        rx.vstack(
            *elements,
            spacing="5",  # VStack spacing: valores literales '0'-'9'
            width="100%",
            align_items="center"
        ),
        **kwargs
    )

