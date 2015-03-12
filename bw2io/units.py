UNITS_NORMALIZATION = {
    "bq": u"Becquerel",
    "h": u"hour",
    "ha": u"hectare",
    "hr": u"hour",
    "kbq": u"kilo Becquerel",
    "kg": u"kilogram",
    "km": u"kilometer",
    "kwh": u"kilowatt hour",
    "l": u"litre",
    "lu": u"livestock unit",
    "m": u"meter",
    "m*year": u"meter-year",
    "m2": u"square meter",
    "m2*year": u"square meter-year",
    "m2a": u"square meter-year",
    "m3": u"cubic meter",
    "m3*year": u"cubic meter-year",
    "m3a": u"cubic meter-year",
    "ma": u"meter-year",
    "metric ton*km": u"ton kilometer",
    "mj": u"megajoule",
    "my": u"meter-year",
    "nm3": u"cubic meter",
    "p": u"unit",
    "personkm": u"person kilometer",
    "pkm": u"person kilometer",
    "tkm": u"ton kilometer",
    "vkm": u"vehicle kilometer",
    'kg swu': u"kilogram separative work unit",
    'km*year': u"kilometer-year",
    'metric ton*km': u"ton kilometer",
    'person*km': u"person kilometer",
}

normalize_units = lambda x: UNITS_NORMALIZATION.get(x.lower(), x)
