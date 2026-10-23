"""Content for the Horizon Properties site.

This module is the single source of truth for every piece of editorial content
on the public site: brand details, navigation, the property portfolio, agents,
team members, services and the values section.

Everything is exposed through the small helper functions at the bottom of the
file, so the views never touch the raw dictionaries directly. Swapping the
portfolio for a database later means reimplementing those helpers only.
"""

# ---------------------------------------------------------------------------
# Brand
# ---------------------------------------------------------------------------

SITE = {
    "name": "Horizon Properties",
    "short_name": "Horizon",
    "tagline": "Premium properties in prime locations",
    "description": (
        "Horizon Properties is a boutique brokerage for exceptional homes and "
        "considered investments, working across Austin, California and the "
        "wider United States."
    ),
    "phone": "(555) 246-7890",
    "phone_href": "+15552467890",
    "email": "hello@horizonproperties.com",
    "address_lines": ["1200 Congress Avenue, Suite 2400", "Austin, TX 78701"],
    "hours": "Monday – Saturday · 9:00 – 18:00",
    "licence": "Licensed Texas real estate brokerage · TREC #9012345",
    "social": [
        {"name": "Instagram", "icon": "instagram", "href": "https://instagram.com"},
        {"name": "LinkedIn", "icon": "linkedin", "href": "https://linkedin.com"},
        {"name": "Facebook", "icon": "facebook", "href": "https://facebook.com"},
    ],
}

NAV = [
    ("Home", "/"),
    ("Properties", "/properties"),
    ("About Us", "/about"),
    ("Services", "/services"),
    ("Team", "/team"),
    ("Contact", "/contact"),
]

# ---------------------------------------------------------------------------
# People
# ---------------------------------------------------------------------------

AGENTS = {
    "daniel-morgan": {
        "slug": "daniel-morgan",
        "name": "Daniel Morgan",
        "role": "Managing Director",
        "photo": "img/portrait-03.jpg",
        "email": "daniel@horizonproperties.com",
        "phone": "+1 (555) 246-7890",
        "linkedin": "https://linkedin.com",
        "bio": (
            "Daniel founded Horizon Properties in 2007 and has since advised on "
            "more than $900M of residential transactions across Texas."
        ),
    },
    "olivia-carter": {
        "slug": "olivia-carter",
        "name": "Olivia Carter",
        "role": "Luxury Property Advisor",
        "photo": "img/portrait-02.jpg",
        "email": "olivia@horizonproperties.com",
        "phone": "+1 (555) 246-7891",
        "linkedin": "https://linkedin.com",
        "bio": (
            "Olivia represents architect-designed homes on the West Coast, with "
            "a particular eye for light, proportion and long-term value."
        ),
    },
    "james-wilson": {
        "slug": "james-wilson",
        "name": "James Wilson",
        "role": "Investment Consultant",
        "photo": "img/portrait-01.jpg",
        "email": "james@horizonproperties.com",
        "phone": "+1 (555) 246-7892",
        "linkedin": "https://linkedin.com",
        "bio": (
            "James builds and reviews income-producing property portfolios for "
            "private clients and family offices."
        ),
    },
    "sophia-bennett": {
        "slug": "sophia-bennett",
        "name": "Sophia Bennett",
        "role": "Senior Property Specialist",
        "photo": "img/portrait-04.jpg",
        "email": "sophia@horizonproperties.com",
        "phone": "+1 (555) 246-7893",
        "linkedin": "https://linkedin.com",
        "bio": (
            "Sophia guides first-time luxury buyers and relocation clients from "
            "first viewing to closing day."
        ),
    },
}

TEAM_ORDER = ["daniel-morgan", "olivia-carter", "james-wilson", "sophia-bennett"]

# ---------------------------------------------------------------------------
# Portfolio
# ---------------------------------------------------------------------------

PROPERTIES = [
    {
        "slug": "lakeside-modern-villa",
        "name": "Lakeside Modern Villa",
        "type": "Villa",
        "status": "Exclusive",
        "featured": True,
        "city": "Austin",
        "region": "Texas",
        "country": "USA",
        "neighbourhood": "Lake Austin",
        "price": 2350000,
        "price_label": "$2.35 Million",
        "price_short": "$2.35M",
        "beds": 5,
        "baths": 5,
        "sqft": 6200,
        "lot": "0.82 acres",
        "garage": 3,
        "year": 2021,
        "agent": "olivia-carter",
        "images": [
            "img/exterior-01.jpg",
            "img/exterior-02.jpg",
            "img/exterior-03.jpg",
            "img/interior-01.jpg",
            "img/interior-02.jpg",
        ],
        "summary": (
            "A cantilevered lakeside villa in warm cedar and glass, designed for "
            "evenings that begin on the water and end by the fire."
        ),
        "description": [
            "Set on a quiet stretch of Lake Austin, this five-bedroom villa opens "
            "through full-height glazing onto a stone terrace and an infinity pool "
            "that appears to spill into the lake itself. The architecture is "
            "deliberately restrained: warm cedar cladding, dark steel frames and "
            "floor-to-ceiling glass that keeps the water in view from almost every room.",
            "The main level is arranged as one continuous living space — kitchen, "
            "dining and lounge — with a library and guest suite tucked behind a "
            "floating oak wall. Upstairs, the primary suite occupies the whole "
            "southern wing with a private terrace and a spa bathroom in honed limestone.",
        ],
        "features": [
            "Full-height glazing throughout",
            "Infinity-edge pool and lake dock",
            "Chef's kitchen with butler's pantry",
            "Primary suite with private terrace",
            "Home office and library",
            "Triple garage with EV charging",
        ],
        "amenities": [
            "Infinity pool",
            "Private boat dock",
            "Wine room",
            "Home cinema",
            "Gym",
            "Smart lighting and climate",
            "Outdoor kitchen",
            "Gated entry",
        ],
    },
    {
        "slug": "pacific-glass-house",
        "name": "Pacific Glass House",
        "type": "House",
        "status": "For Sale",
        "featured": True,
        "city": "Malibu",
        "region": "California",
        "country": "USA",
        "neighbourhood": "Point Dume",
        "price": 4800000,
        "price_label": "$4.8 Million",
        "price_short": "$4.8M",
        "beds": 5,
        "baths": 6,
        "sqft": 7400,
        "lot": "1.1 acres",
        "garage": 4,
        "year": 2022,
        "agent": "daniel-morgan",
        "images": [
            "img/exterior-04.jpg",
            "img/interior-09.jpg",
            "img/interior-10.jpg",
            "img/interior-03.jpg",
        ],
        "summary": (
            "A sculptural white residence above Point Dume, arranged around a "
            "courtyard pool and framed views of the Pacific."
        ),
        "description": [
            "Pacific Glass House is a study in light and volume: a cubist white "
            "composition that steps down the hillside, with a water sculpture at "
            "its centre and glazed galleries connecting each level.",
            "Interiors are calm and pale — micro-cement floors, oak joinery and "
            "sliding walls — with a double-height living room that opens entirely "
            "to the pool terrace. The lower level holds a wellness suite, wine "
            "cellar and a media room that doubles as a screening space.",
        ],
        "features": [
            "Ocean and coastline views",
            "Courtyard pool with water feature",
            "Double-height living room",
            "Wellness suite with sauna",
            "Wine cellar and tasting area",
            "Four-car garage",
        ],
        "amenities": [
            "Courtyard pool",
            "Sauna and steam room",
            "Screening room",
            "Wine cellar",
            "Guest house",
            "Rooftop terrace",
            "Solar array",
            "Gated motor court",
        ],
    },
    {
        "slug": "desert-horizon-estate",
        "name": "Desert Horizon Estate",
        "type": "Estate",
        "status": "For Sale",
        "featured": True,
        "city": "Scottsdale",
        "region": "Arizona",
        "country": "USA",
        "neighbourhood": "Paradise Valley",
        "price": 3150000,
        "price_label": "$3.15 Million",
        "price_short": "$3.15M",
        "beds": 6,
        "baths": 5,
        "sqft": 8100,
        "lot": "1.6 acres",
        "garage": 4,
        "year": 2020,
        "agent": "james-wilson",
        "images": [
            "img/exterior-05.jpg",
            "img/interior-04.jpg",
            "img/interior-11.jpg",
            "img/interior-12.jpg",
        ],
        "summary": (
            "A low-slung desert estate where white volumes, water and native "
            "planting meet the Sonoran horizon."
        ),
        "description": [
            "Desert Horizon Estate is built on one quiet horizontal line. Long "
            "white volumes frame the pool terrace, with deep overhangs keeping "
            "the interiors cool through the Arizona summer.",
            "Six bedrooms are arranged in two wings around a central gallery, "
            "leaving the living spaces open to the garden and the mountain views "
            "beyond. Materials are deliberately tactile: travertine, lime plaster "
            "and blackened steel.",
        ],
        "features": [
            "Mountain and sunset views",
            "Deep cantilevered overhangs",
            "Reflecting pool and spa",
            "Casita for guests",
            "Chef's kitchen with catering pantry",
            "Detached four-car garage",
        ],
        "amenities": [
            "Infinity pool and spa",
            "Casita",
            "Outdoor kitchen",
            "Fire terrace",
            "Desert botanical garden",
            "Home gym",
            "Motor court",
            "Full home automation",
        ],
    },
    {
        "slug": "oceanfront-residence",
        "name": "Oceanfront Residence",
        "type": "Waterfront Residence",
        "status": "Exclusive",
        "featured": True,
        "city": "Miami",
        "region": "Florida",
        "country": "USA",
        "neighbourhood": "Bal Harbour",
        "price": 5200000,
        "price_label": "$5.2 Million",
        "price_short": "$5.2M",
        "beds": 6,
        "baths": 7,
        "sqft": 8900,
        "lot": "0.9 acres",
        "garage": 3,
        "year": 2023,
        "agent": "sophia-bennett",
        "images": [
            "img/exterior-06.jpg",
            "img/interior-05.jpg",
            "img/interior-07.jpg",
            "img/interior-08.jpg",
        ],
        "summary": (
            "A bright, palm-framed residence a few steps from the sand, with a "
            "loggia built for long lunches and late swims."
        ),
        "description": [
            "Oceanfront Residence opens on both sides: the ocean to the east, and "
            "a sheltered garden pool to the west. Between them sit generous, "
            "sun-filled rooms with white oak floors and coral stone bathrooms.",
            "The loggia runs the full width of the house and is served by an "
            "outdoor kitchen and bar, making it the natural centre of the home. "
            "Six bedroom suites include a ground-floor guest wing and a primary "
            "suite with its own terrace above the pool.",
        ],
        "features": [
            "Direct beach access",
            "Loggia with outdoor kitchen",
            "Garden pool and sun terrace",
            "Primary suite with private terrace",
            "Elevator to all floors",
            "Impact-rated glazing",
        ],
        "amenities": [
            "Heated pool",
            "Outdoor kitchen and bar",
            "Summer kitchen",
            "Pool cabana",
            "Gym",
            "Staff suite",
            "Generator",
            "Security system",
        ],
    },
    {
        "slug": "modern-hillside-retreat",
        "name": "Modern Hillside Retreat",
        "type": "Villa",
        "status": "For Sale",
        "featured": True,
        "city": "Los Angeles",
        "region": "California",
        "country": "USA",
        "neighbourhood": "Hollywood Hills",
        "price": 3750000,
        "price_label": "$3.75 Million",
        "price_short": "$3.75M",
        "beds": 4,
        "baths": 5,
        "sqft": 5400,
        "lot": "0.6 acres",
        "garage": 2,
        "year": 2019,
        "agent": "olivia-carter",
        "images": [
            "img/exterior-07.jpg",
            "img/interior-02.jpg",
            "img/interior-06.jpg",
            "img/interior-12.jpg",
        ],
        "summary": (
            "A stone-and-glass retreat terraced into the hillside, with city "
            "lights below and canyon quiet above."
        ),
        "description": [
            "Built into a steep Hollywood Hills lot, the house steps down in "
            "three terraces, each opening to a different view — canyon, city and "
            "sky. Stone cladding grounds the structure in the hillside while "
            "glass keeps the outlook unobstructed.",
            "Living, dining and kitchen share one level with a long island and a "
            "wall of sliding doors. Below, a media lounge and two guest suites "
            "open onto the pool deck; the primary suite occupies the top floor.",
        ],
        "features": [
            "Terraced hillside site",
            "City-light views",
            "Stone and glass elevations",
            "Pool deck with lounge terrace",
            "Media lounge",
            "Two-car garage plus motor court",
        ],
        "amenities": [
            "Pool and sun deck",
            "Media lounge",
            "Outdoor fireplace",
            "Chef's kitchen",
            "Wine wall",
            "Guest suites",
            "Laundry and mud room",
            "Gated entry",
        ],
    },
    {
        "slug": "palm-garden-residence",
        "name": "Palm Garden Residence",
        "type": "Estate",
        "status": "For Sale",
        "featured": True,
        "city": "Beverly Hills",
        "region": "California",
        "country": "USA",
        "neighbourhood": "Trousdale",
        "price": 6400000,
        "price_label": "$6.4 Million",
        "price_short": "$6.4M",
        "beds": 7,
        "baths": 8,
        "sqft": 11200,
        "lot": "1.9 acres",
        "garage": 5,
        "year": 2022,
        "agent": "daniel-morgan",
        "images": [
            "img/exterior-08.jpg",
            "img/interior-01.jpg",
            "img/interior-06.jpg",
            "img/interior-10.jpg",
        ],
        "summary": (
            "A single-storey estate wrapped around a mature palm garden, with "
            "glass doors that disappear into the walls."
        ),
        "description": [
            "Palm Garden Residence is organised as a courtyard house: seven "
            "bedroom suites arranged around a garden and pool, so every room has "
            "its own green outlook and the garden stays private.",
            "Sliding glass walls open the living and dining rooms fully to the "
            "terrace, and the kitchen is supported by a catering kitchen and "
            "service entry. A separate pavilion holds the gym, spa and guest suite.",
        ],
        "features": [
            "Courtyard plan with palm garden",
            "Full-width sliding glass walls",
            "Catering kitchen",
            "Spa pavilion with gym",
            "Five-car garage",
            "Motor court and gated drive",
        ],
        "amenities": [
            "Pool and spa",
            "Spa pavilion",
            "Home gym",
            "Guest suite",
            "Catering kitchen",
            "Outdoor dining terrace",
            "Rose and palm garden",
            "Full security system",
        ],
    },
    {
        "slug": "contemporary-lake-house",
        "name": "Contemporary Lake House",
        "type": "Lake House",
        "status": "For Sale",
        "featured": False,
        "city": "Lake Tahoe",
        "region": "Nevada",
        "country": "USA",
        "neighbourhood": "Glenbrook",
        "price": 2950000,
        "price_label": "$2.95 Million",
        "price_short": "$2.95M",
        "beds": 4,
        "baths": 4,
        "sqft": 4300,
        "lot": "1.2 acres",
        "garage": 2,
        "year": 2018,
        "agent": "james-wilson",
        "images": [
            "img/exterior-09.jpg",
            "img/exterior-10.jpg",
            "img/interior-03.jpg",
            "img/interior-05.jpg",
        ],
        "summary": (
            "A contemporary lodge between the pines, with a double-height living "
            "room and a lakeside deck for every season."
        ),
        "description": [
            "Set among mature pines above Glenbrook, the house takes the shape of "
            "a modern lodge — dark timber, steep roofs and a warm interior that "
            "works as well in February as it does in July.",
            "A double-height living room with a stone hearth is the centre of the "
            "plan, opening to a lakeside deck on one side and a protected "
            "courtyard on the other. Four bedrooms include a bunk room for guests "
            "and a primary suite with its own balcony.",
        ],
        "features": [
            "Double-height living room",
            "Stone hearth and timber ceilings",
            "Lakeside deck and courtyard",
            "Bunk room for guests",
            "Heated driveway",
            "Ski and paddleboard store",
        ],
        "amenities": [
            "Wood-burning hearth",
            "Lakeside deck",
            "Private buoy",
            "Mud room",
            "Heated floors",
            "Wine fridge",
            "Fire pit terrace",
            "Two-car garage",
        ],
    },
    {
        "slug": "architectural-downtown-penthouse",
        "name": "Architectural Downtown Penthouse",
        "type": "Penthouse",
        "status": "For Sale",
        "featured": False,
        "city": "Austin",
        "region": "Texas",
        "country": "USA",
        "neighbourhood": "Downtown",
        "price": 1850000,
        "price_label": "$1.85 Million",
        "price_short": "$1.85M",
        "beds": 3,
        "baths": 3,
        "sqft": 3200,
        "lot": "—",
        "garage": 2,
        "year": 2023,
        "agent": "sophia-bennett",
        "images": [
            "img/interior-01.jpg",
            "img/exterior-10.jpg",
            "img/interior-04.jpg",
            "img/interior-07.jpg",
        ],
        "summary": (
            "A full-floor penthouse above downtown Austin, wrapping 360 degrees "
            "of glazing around a private sky terrace."
        ),
        "description": [
            "Occupying the whole of the twenty-fourth floor, the penthouse is "
            "arranged around a central core so that living spaces and terraces "
            "wrap the entire perimeter of the building.",
            "Interiors are quiet and precise: pale oak floors, plaster walls and "
            "a monolithic kitchen island. A private sky terrace with an outdoor "
            "kitchen faces the sunset, and the building offers concierge, "
            "valet parking and a residents' pool.",
        ],
        "features": [
            "Full-floor plan with 360° glazing",
            "Private sky terrace",
            "Concierge and valet parking",
            "Residents' pool and fitness club",
            "Two reserved parking spaces",
            "Dedicated lift access",
        ],
        "amenities": [
            "Sky terrace",
            "Outdoor kitchen",
            "Concierge",
            "Residents' pool",
            "Fitness club",
            "Secure parking",
            "Storage suite",
            "Pet friendly building",
        ],
    },
]

# ---------------------------------------------------------------------------
# Services, values and statistics
# ---------------------------------------------------------------------------

SERVICES = [
    {
        "slug": "luxury-home-sales",
        "title": "Luxury Home Sales",
        "summary": (
            "Discreet representation for architect-designed homes, from first "
            "valuation to closing day."
        ),
        "image": "img/exterior-05.jpg",
        "points": ["Private and off-market sales", "Global buyer network", "Full transaction management"],
    },
    {
        "slug": "property-investment",
        "title": "Property Investment",
        "summary": (
            "Yield analysis, portfolio building and acquisition strategy for "
            "private clients and family offices."
        ),
        "image": "img/interior-09.jpg",
        "points": ["Yield and risk modelling", "Portfolio reviews", "Off-market acquisitions"],
    },
    {
        "slug": "property-marketing",
        "title": "Property Marketing",
        "summary": (
            "Editorial photography, film and campaign design that present a "
            "property at its best."
        ),
        "image": "img/exterior-07.jpg",
        "points": ["Architectural photography", "Film and drone", "Print and digital campaigns"],
    },
    {
        "slug": "real-estate-advisory",
        "title": "Real Estate Advisory",
        "summary": (
            "Independent advice on structuring, timing and negotiation for "
            "significant residential assets."
        ),
        "image": "img/interior-06.jpg",
        "points": ["Acquisition strategy", "Negotiation support", "Due diligence"],
    },
    {
        "slug": "property-valuation",
        "title": "Property Valuation",
        "summary": (
            "Detailed market appraisals grounded in comparable sales and current "
            "buyer demand."
        ),
        "image": "img/interior-11.jpg",
        "points": ["Comparable sales analysis", "Written appraisal", "Annual portfolio review"],
    },
    {
        "slug": "relocation-services",
        "title": "Relocation Services",
        "summary": (
            "End-to-end support for families and executives moving to a new city "
            "or country."
        ),
        "image": "img/exterior-04.jpg",
        "points": ["Neighbourhood guidance", "School and lifestyle research", "Settling-in support"],
    },
]

VALUES = [
    {
        "title": "Architectural understanding",
        "text": (
            "We represent buildings we genuinely admire, and we can explain why "
            "they will hold their value."
        ),
    },
    {
        "title": "Discretion",
        "text": (
            "A significant share of our work is off-market. Nothing about your "
            "sale or purchase leaves the room without your approval."
        ),
    },
    {
        "title": "One advisor, start to finish",
        "text": (
            "You work with the same senior advisor from valuation to keys, "
            "supported by our research and marketing teams."
        ),
    },
    {
        "title": "Evidence, not opinion",
        "text": (
            "Every valuation is built from comparable sales, days-on-market data "
            "and current buyer demand — never instinct alone."
        ),
    },
]

STATS = [
    {"value": "$2.4B", "label": "Residential sales advised"},
    {"value": "18", "label": "Years in prime markets"},
    {"value": "1,240", "label": "Homes bought and sold"},
    {"value": "97%", "label": "Of asking price achieved"},
]

ABOUT_IMAGES = {
    "main": "img/exterior-06.jpg",
    "side": "img/about-side.jpg",
}

HERO_IMAGE = {
    "src": "img/hero-villa-dusk.jpg",
    "alt": "A modern lakeside villa at dusk, interior lit, reflected in a still pool",
}

# ---------------------------------------------------------------------------
# Filter option lists (derived from the portfolio where possible)
# ---------------------------------------------------------------------------

PRICE_RANGES = [
    ("", "Any price", None, None),
    ("under-2m", "Under $2M", None, 2000000),
    ("2m-4m", "$2M – $4M", 2000000, 4000000),
    ("4m-6m", "$4M – $6M", 4000000, 6000000),
    ("6m-plus", "$6M and above", 6000000, None),
]

BED_OPTIONS = [("", "Any beds"), ("3", "3+ beds"), ("4", "4+ beds"), ("5", "5+ beds"), ("6", "6+ beds")]
BATH_OPTIONS = [("", "Any baths"), ("3", "3+ baths"), ("4", "4+ baths"), ("5", "5+ baths"), ("6", "6+ baths")]

SORT_OPTIONS = [
    ("featured", "Featured first"),
    ("price-asc", "Price: low to high"),
    ("price-desc", "Price: high to low"),
    ("year-desc", "Newest built"),
    ("size-desc", "Largest first"),
]


# ---------------------------------------------------------------------------
# Helpers used by the views
# ---------------------------------------------------------------------------

def all_properties():
    """Return the full portfolio, featured listings first."""
    return sorted(PROPERTIES, key=lambda p: (not p["featured"], p["price"]), reverse=False)


def featured_properties(limit=6):
    return [p for p in PROPERTIES if p["featured"]][:limit]


def get_property(slug):
    for item in PROPERTIES:
        if item["slug"] == slug:
            return item
    return None


def similar_properties(prop, limit=3):
    others = [p for p in PROPERTIES if p["slug"] != prop["slug"]]
    same_type = [p for p in others if p["type"] == prop["type"]]
    same_city = [p for p in others if p["city"] == prop["city"] and p not in same_type]
    rest = [p for p in others if p not in same_type and p not in same_city]
    return (same_type + same_city + rest)[:limit]


def get_agent(slug):
    return AGENTS.get(slug, AGENTS[TEAM_ORDER[0]])


def team_members():
    return [AGENTS[slug] for slug in TEAM_ORDER]


def locations():
    """Unique (city, region) pairs for the location filter."""
    seen, out = set(), []
    for p in PROPERTIES:
        key = (p["city"], p["region"])
        if key not in seen:
            seen.add(key)
            out.append({"value": f"{p['city']}|{p['region']}", "label": f"{p['city']}, {p['region']}"})
    return sorted(out, key=lambda item: item["label"])


def property_types():
    return sorted({p["type"] for p in PROPERTIES})


def filter_properties(args):
    """Apply the browse-page filters to the portfolio and return (items, meta)."""
    query = (args.get("q") or "").strip().lower()
    location = (args.get("location") or "").strip()
    ptype = (args.get("type") or "").strip()
    beds = args.get("beds") or ""
    baths = args.get("baths") or ""
    price_key = (args.get("price") or "").strip()
    sort = (args.get("sort") or "featured").strip()

    price_min = price_max = None
    for key, _label, low, high in PRICE_RANGES:
        if key and key == price_key:
            price_min, price_max = low, high

    city = region = None
    if "|" in location:
        city, region = location.split("|", 1)

    items = []
    for p in PROPERTIES:
        if query:
            haystack = " ".join(
                [
                    p["name"], p["type"], p["city"], p["region"], p["country"],
                    p["neighbourhood"], p["summary"],
                ]
            ).lower()
            if query not in haystack:
                continue
        if city and (p["city"] != city or p["region"] != region):
            continue
        if ptype and p["type"] != ptype:
            continue
        if beds and p["beds"] < int(beds):
            continue
        if baths and p["baths"] < int(baths):
            continue
        if price_min is not None and p["price"] < price_min:
            continue
        if price_max is not None and p["price"] > price_max:
            continue
        items.append(p)

    sorters = {
        "price-asc": lambda p: p["price"],
        "price-desc": lambda p: -p["price"],
        "year-desc": lambda p: -p["year"],
        "size-desc": lambda p: -p["sqft"],
        "featured": lambda p: (not p["featured"], -p["price"]),
    }
    items.sort(key=sorters.get(sort, sorters["featured"]))

    active = sum(
        1 for value in (query, location, ptype, beds, baths, price_key) if value
    )
    return items, {"count": len(items), "active_filters": active, "sort": sort}
