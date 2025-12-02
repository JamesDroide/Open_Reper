# ============================================
# PALETA DE COLORES
# ============================================

# Colores principales
BLUE_DARK = "#2A5C9A"
BLUE_HOVER = "#1E3A5F"
BLUE_DARK_HOVER = "#152942"
ORANGE = "#F24100"
ORANGE_HOVER = "#E03D00"
WHITE = "#FFFFFF"
GRAY = "#D1E0E0"
LIGHT_SQUARE = "#F0D9B5"
DARK_SQUARE = "#B58863"
SELECTED_SQUARE = "#BBCB2B"
LEGAL_MOVE_SQUARE = "#86A666"
GREEN = "#4CAF50"
GREEN_HOVER = "#388E3C"

# Colores semánticos (para estados)
COLOR_SUCCESS = "#4CAF50"
COLOR_ERROR = "#E53935"
COLOR_WARNING = "#FFC107"
COLOR_INFO = "#2196F3"

# ============================================
# TIPOGRAFÍA
# ============================================

# Fuente principal
FONT_FAMILY = '"Libre Baskerville", serif'
FONT_FAMILY_MONO = '"Courier New", monospace'

# Tamaños de fuente responsivos [mobile, tablet, desktop, desktop-xl]
FONT_XXS = ["0.65em", "0.7em", "0.75em", "0.8em"]
FONT_XS = ["0.75em", "0.8em", "0.85em", "0.9em"]
FONT_SM = ["0.85em", "0.9em", "0.95em", "1em"]
FONT_MD = ["1em", "1.05em", "1.1em", "1.15em"]
FONT_LG = ["1.2em", "1.3em", "1.4em", "1.5em"]
FONT_XL = ["1.4em", "1.6em", "1.8em", "2em"]
FONT_XXL = ["1.8em", "2em", "2.4em", "2.8em"]

# Pesos de fuente
FONT_WEIGHT_NORMAL = "400"
FONT_WEIGHT_MEDIUM = "500"
FONT_WEIGHT_SEMIBOLD = "600"
FONT_WEIGHT_BOLD = "700"

# ============================================
# SISTEMA DE ESPACIADO (Escala de 4px)
# ============================================
# Formato: [mobile, tablet, desktop, desktop-xl]

SPACE_XXS = ["2px", "2px", "4px", "4px"]
SPACE_XS = ["4px", "6px", "8px", "8px"]
SPACE_SM = ["8px", "10px", "12px", "16px"]
SPACE_MD = ["12px", "14px", "16px", "20px"]
SPACE_LG = ["16px", "20px", "24px", "32px"]
SPACE_XL = ["24px", "28px", "32px", "40px"]
SPACE_XXL = ["32px", "40px", "48px", "64px"]

# Espaciado específico (em-based para escalabilidad)
SPACING_XS = ["0.3em", "0.4em", "0.5em", "0.6em"]
SPACING_SM = ["0.5em", "0.6em", "0.7em", "0.8em"]
SPACING_MD = ["0.7em", "0.8em", "0.9em", "1em"]
SPACING_LG = ["1em", "1.2em", "1.4em", "1.6em"]
SPACING_XL = ["1.5em", "1.8em", "2em", "2.5em"]

# Padding responsivo
PADDING_XS = ["0.3em", "0.4em", "0.5em", "0.6em"]
PADDING_SM = ["0.5em", "0.6em", "0.7em", "0.8em"]
PADDING_MD = ["0.7em", "0.9em", "1em", "1.2em"]
PADDING_LG = ["1em", "1.3em", "1.5em", "2em"]
PADDING_XL = ["1.5em", "2em", "2.5em", "3em"]

# ============================================
# ANCHOS Y ALTURAS RESPONSIVOS
# ============================================

# Anchos de contenedores
WIDTH_FULL = "100%"
WIDTH_FORM = ["95%", "350px", "400px", "450px"]
WIDTH_BOARD = ["95%", "380px", "450px", "520px"]
WIDTH_TABLE = ["95%", "280px", "320px", "350px"]
WIDTH_CARD = ["100%", "300px", "350px", "400px"]

# Anchos máximos para contenedores
MAX_WIDTH_SM = "600px"
MAX_WIDTH_MD = "800px"
MAX_WIDTH_LG = "1000px"
MAX_WIDTH_XL = "1200px"
MAX_WIDTH_XXL = "1400px"

# Tamaños de elementos específicos
SIZE_LOGO = ["80px", "100px", "120px", "140px"]
SIZE_PAWN = ["36px", "42px", "48px", "54px"]
SIZE_PIECE = ["40px", "45px", "50px", "56px"]
SIZE_BUTTON_SM = ["32px", "36px", "40px", "44px"]
SIZE_BUTTON_MD = ["40px", "44px", "48px", "52px"]
SIZE_BUTTON_LG = ["48px", "52px", "56px", "60px"]

# Alturas
HEIGHT_INPUT = ["40px", "44px", "48px", "52px"]
HEIGHT_TEXTAREA = ["120px", "140px", "160px", "180px"]

# ============================================
# BORDER RADIUS
# ============================================

RADIUS_SM = ["4px", "6px", "8px", "8px"]
RADIUS_MD = ["6px", "8px", "10px", "12px"]
RADIUS_LG = ["8px", "10px", "12px", "16px"]
RADIUS_XL = ["12px", "16px", "20px", "24px"]
RADIUS_FULL = "9999px"

# ============================================
# SOMBRAS (Box Shadows)
# ============================================

SHADOW_NONE = "none"
SHADOW_XS = "0 1px 2px rgba(0, 0, 0, 0.05)"
SHADOW_SM = "0 2px 4px rgba(0, 0, 0, 0.08)"
SHADOW_MD = "0 4px 6px rgba(0, 0, 0, 0.1)"
SHADOW_LG = "0 8px 12px rgba(0, 0, 0, 0.12)"
SHADOW_XL = "0 12px 24px rgba(0, 0, 0, 0.15)"
SHADOW_XXL = "0 20px 40px rgba(0, 0, 0, 0.2)"

# Sombras de color (para hover states)
SHADOW_PRIMARY = "0 4px 12px rgba(42, 92, 154, 0.3)"
SHADOW_SECONDARY = "0 4px 12px rgba(242, 65, 0, 0.3)"
SHADOW_SUCCESS = "0 4px 12px rgba(76, 175, 80, 0.3)"

# ============================================
# TRANSICIONES Y ANIMACIONES
# ============================================
# Duración en segundos [mobile, tablet, desktop]
# Mobile más rápido para ahorrar batería

TRANSITION_FAST = ["0.1s", "0.15s", "0.2s"]
TRANSITION_NORMAL = ["0.2s", "0.25s", "0.3s"]
TRANSITION_SLOW = ["0.3s", "0.35s", "0.4s"]

# Timing functions
EASE_IN = "ease-in"
EASE_OUT = "ease-out"
EASE_IN_OUT = "ease-in-out"
EASE_BOUNCE = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"

# ============================================
# BREAKPOINTS (para referencia)
# ============================================
# Estos están definidos en rxconfig.py pero aquí para documentación

BREAKPOINT_MOBILE = "480px"
BREAKPOINT_TABLET = "768px"
BREAKPOINT_DESKTOP = "1024px"
BREAKPOINT_DESKTOP_LG = "1440px"
BREAKPOINT_DESKTOP_XL = "1920px"

# ============================================
# Z-INDEX (Sistema de capas)
# ============================================

Z_BACKGROUND = -1
Z_NORMAL = 0
Z_DROPDOWN = 100
Z_STICKY = 200
Z_MODAL_BACKDROP = 300
Z_MODAL = 400
Z_POPOVER = 500
Z_TOOLTIP = 600
Z_NOTIFICATION = 700
