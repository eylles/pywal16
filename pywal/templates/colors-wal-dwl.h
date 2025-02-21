/* Taken from https://github.com/djpohly/dwl/issues/466 */
#define COLOR(hex)    {{ ((hex >> 24) & 0xFF) / 255.0f, \
                        ((hex >> 16) & 0xFF) / 255.0f, \
                        ((hex >> 8) & 0xFF) / 255.0f, \
                        (hex & 0xFF) / 255.0f }}

static const float rootcolor[]             = COLOR(0x{color0.strip}ff);
static uint32_t colors[][3]                = {{
	/*               fg          bg          border    */
	[SchemeNorm] = {{ 0x{color15.strip}ff, 0x{color0.strip}ff, 0x{color8.strip}ff }},
	[SchemeSel]  = {{ 0x{color15.strip}ff, 0x{color2.strip}ff, 0x{color1.strip}ff }},
	[SchemeUrg]  = {{ 0x{color15.strip}ff, 0x{color1.strip}ff, 0x{color2.strip}ff }},
}};
