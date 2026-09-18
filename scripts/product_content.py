"""Concise storefront copy and verifiable product details from the catalog."""
import re

STORIES = {
    'ilm-606v-dual-sports-helmets': 'A dual sport helmet for riders who move between paved roads and rougher routes. Its visor setup, washable lining and ventilation are designed for longer days in the saddle.',
    'ilm-ws-902-dual-sports-helmet': 'The WS-902 brings an adventure style helmet to everyday and touring rides. A wide view, dual visor setup and removable lining make it practical across changing conditions.',
    'ilm-mf-568-full-face-helmet': 'A full face helmet with a bold finish and an ABS shell. It is made for riders who want protection, ventilation and a clear view in one road-ready design.',
    'ilm-129-helmet': 'A streamlined helmet for daily riding and longer trips. Its lightweight shell and removable interior make comfort and care easier to manage.',
    'ilm-902l-modular-helmet': 'A modular helmet that lets riders switch between open and full coverage on the road. Its adjustable strap and removable cheek pads support a more personal fit.',
    'ilm-mf-509-full-face': 'The MF-509 is a full face helmet built around a secure fit and road comfort. Explore the visor, lining and finish options before choosing your size.',
    'ilm-mf-567-cobra-camelion-helmet': 'A full face helmet with the Cobra Chameleon graphic. Its protective shell and ventilation suit riders who want a distinctive look for road use.',
    'ilm-z-501-helmet': 'The Z-501 combines full face coverage with a bright Armor Red finish. Its shell, visor and comfort lining are designed for regular motorcycle rides.',
    'ilm-jk-313-helmet': 'A road helmet supplied with clear and smoked visors. Its streamlined shell and quick-release strap make it a practical choice for changing light and daily use.',
    'ilm-mf-510-helmet': 'The MF-510 pairs a full face shape with ILM impact-management technology. Review the fit, visor and available finish with Sherpa Quest before ordering.',
    'rhinowalk-10ltr-tail-bag': 'A compact 10L tail bag for commutes and short rides. It keeps essentials on the motorcycle and includes a removable waterproof liner.',
    'rhinowalk-20ltr-tail-bag': 'This 20L tail bag adds flexible storage to the rear seat. Carry it off the bike as a shoulder bag or backpack, with a removable liner for wet weather.',
    'rhinowalk-30ltr-tail-bag': 'A roomier 30L tail bag for rides that need extra layers and essentials. Its removable liner and carry options make it useful on and off the motorcycle.',
    'rhinowalk-28ltr-saddle-bag': 'A rackless side luggage system for touring and adventure riding. The paired bags give riders organized storage without a dedicated side rack.',
    'warrior-series-waterproof-motorcycle-duffel-bag-40l': 'A 40L duffel for rear-seat or rack storage. Its roll-top construction keeps touring gear organized through changing weather.',
    'rhinowalk-1-5ltr-motorcycle-bottle-holder': 'A small insulated holder for a drink or snack on the road. It expands to suit different loads and attaches to compatible MOLLE luggage.',
    'mechanic-series-6l-motorcycle-crash-bar-bag-with-waterproof-liner': 'A compact 6L bag for tools, gloves and other quick-access gear. A removable waterproof liner helps protect the contents.',
    'mechanic-series-quick-release-motorcycle-panniers-35l': 'A 35L side bag with a quick-release mounting setup. It provides structured touring storage and can be removed from a compatible rack when the ride ends.',
    'expandable-motorcycle-tail-bag-40-60ltr': 'A high-capacity tail bag range for extended rides. Expandable side sections let riders add room as their load changes.',
    'mechanic-series-9l-motorcycle-tank-bag-with-1-5l-hydration-bladder': 'A 9L tank bag that keeps small essentials close at hand. It includes a 1.5L hydration bladder and layered compartments for organization.',
    'warrior-series-24l-waterproof-motorcycle-side-bag': 'A 24L soft side bag for touring and commuting. Its waterproof construction offers flexible luggage space for one side or a matched pair.',
    '25-32l-quick-release-motorcycle-side-bag': 'A side bag that expands from 25L to 32L. Quick-release hooks make it easier to remove the bag from a compatible rack.',
    'mechanic-series-mjx2010-2l-motorcycle-handlebar-bag': 'A 2L handlebar bag for items you need during a ride. Its structured body keeps compact essentials within reach at the cockpit.',
    'rhinowalk-6l-waterproof-motorcycle-crash-bar-bag': 'A 6L roll-top dry bag for crash-bar storage. Integrated straps help secure tools or rain gear where they are easy to reach.',
    'rhinowalk-mechanic-series-23l-motorcycle-riding-backpack': 'A 23L backpack made around riding comfort and organized storage. Ventilated back support and a quick-release chest buckle help on longer days.',
    'universal-motorcycle-saddlebag-mounting-base': 'An adjustable base for compatible soft side bags. Reinforced webbing and attachment points help create a stable two-sided luggage setup.',
    'rhinowalk-26l-waterproof-motorcycle-backpack-tail-bag': 'A 26L waterproof bag that switches between backpack and tail-bag use. An external helmet carry option keeps the main compartment free.',
    'traverse-series-10l-adventure-motorcycle-backpack': 'A compact 10L pack for active riding. Its stable harness and hydration routing keep essentials close without a large luggage load.',
    'multi-way-motorcycle-tactical-drop-leg-bag': 'A small personal bag for riding essentials. Adjustable straps let it be worn in different ways when you do not need motorcycle-mounted luggage.',
    'mechanic-series-5-6-5l-magnetic-motorcycle-tank-bag': 'An expandable tank bag for compact front-of-bike storage. Its fuel-cap ring mount keeps the bag secured above the tank.',
    'motorcycle-tool-roll-bag-black': 'A compact roll for organizing roadside tools. Elastic loops and folding panels separate equipment so it is easier to find when needed.',
    'mechanic-series-50-70l-motorcycle-touring-seat-bag': 'A large touring seat bag that expands from about 50L to 70L. Its structured mounting design suits longer journeys with more gear.',
    'feher-ventilated-breathable-sj2311-riding-jacket-aeroflow': 'A ventilated riding jacket for warm weather miles. Mesh airflow, a durable outer fabric and removable protection balance comfort with road use.',
    'feher-jk-033a-terrain-all-season-2-layer-motor-cycle-riding-jacket': 'A two-layer jacket for rides through changing weather. Its waterproof, windproof and insulated design is made for year-round use.',
    'feher-jk-063a-trailguard-3-in-1-all-season-motor-cycle-riding-jacket': 'A versatile three-in-one jacket for changing routes and temperatures. Ventilation and removable layers let riders adjust the setup for the day.',
    'feher-jk059-storm-x': 'A three-layer touring suit for longer journeys. Waterproof construction and protective armor are designed for rides through varied weather.',
    'feher-jk-061-rally-x-3-layer-all-season-motorcycle-touring-jacket': 'A three-layer touring jacket for the long way around. Its weather protection, armor and durable outer fabric suit changing riding conditions.',
    'ilm-adventure-riding-jacket': 'An adventure jacket for riders who need airflow and adaptable weather protection. Its outer shell, mesh and liner support a range of routes.',
    'ilm-motorcycle-rain-suit-stormshield': 'A two-piece rain suit for wet rides. Its waterproof construction and integrated coverage help keep the rider more comfortable when weather turns.',
    'feher-rainsheild': 'A lightweight rain suit that packs for sudden weather changes. Waterproof and windproof materials add a practical layer over riding gear.',
    'alien-monter-howl-classic-glove': 'A leather riding glove with protective knuckle and palm details. Ventilation and touchscreen support add everyday convenience.',
    'alien-monster-howl-fabric-glove': 'A textile riding glove with protective details and a grippy palm. Ventilation and flexible construction suit regular rides.',
    'alien-monster-preadator-evolution': 'A leather riding glove that combines perforation, a durable palm and protective padding. The two photographed finishes let you compare the look before asking about fit.',
    'alien-monster-ultimate-energy': 'A lightweight glove designed for airflow and easy movement. Mesh construction and palm details support comfort and control.',
    'alien-monster-mountain-breeze': 'A leather glove made for grip and airflow. A durable palm and protective details support everyday motorcycle use.',
    'alien-monster-ant-king': 'A leather riding glove with a grippy palm and flexible feel. It is designed for riders who want a secure hold on the controls.',
    'ilm-igoat-skin-leather-gloves': 'A goatskin riding glove with hard-shell knuckle protection. Its leather construction balances durability with a natural feel at the controls.',
    'arcx-l60612-urban-guard': 'A leather riding boot with a clean urban profile. Reinforcement at key areas and a grippy sole support time on and off the motorcycle.',
    'arcx-l54947-ironride': 'A waterproof leather boot for touring and adventure rides. Protective reinforcement and a breathable lining are built for longer days.',
    'arcx-l60024-lunar': 'A waterproof leather touring boot with ankle and heel protection. Side zippers make it easier to put on and adjust.',
    'arcx-l60746-aircore': 'A perforated leather boot for warmer rides. Airflow and protective reinforcement bring road function to a lighter-feeling design.',
    'ilm-mx3a-enduro': 'An enduro boot with molded shin and ankle guards. Its protective construction is intended for more demanding riding conditions.',
    'freedcon-fx': 'An intercom for group rides and shared audio. It supports multiple rider connections, Bluetooth pairing and wet-weather use.',
    'maxto-m2': 'A Bluetooth intercom for communication on group rides. It supports up to six riders and brings audio to the helmet.',
    'jyd-c65': 'A group intercom designed for rides with several people. Its eight-rider network helps a crew stay connected on the road.',
}

NEW_STORIES = {
    'kp101ep01-knee-elbow-guard': 'Protect your knees and elbows with ergonomic guards designed to stay in place on the ride. Their shaped shells and padded construction cover the areas riders reach for first in a fall.',
    'kp16ep16-mx-knee-elbow-guard': 'The KP16EP16 guard set is shaped for dirt riding, with a three-section knee design that bends with your leg. Its hard shell adds impact coverage for more demanding routes.',
    'wt01-motorcycle-lumbar-support': 'The WT01 supports the lower back on long days in the saddle. A firm outer structure and breathable contact panels help distribute pressure without trapping as much heat.',
    'mh01-traillock-pro-phone-mount': 'Keep navigation in sight with a motorcycle phone mount built to reduce vibration at the handlebars. The MH01 secures the phone while leaving it accessible for the next stop.',
    'mh02-traillock-x-pro-phone-camera-mount': 'The MH02 carries a phone and action camera from one motorcycle mounting point. Vibration damping helps keep both devices steadier over uneven roads.',
    'osah-edge-pro-40l-duffel-bag': 'A 40L duffel for touring loads and weekend trips. The Edge Pro gives riders a roomy, weather-ready bag that can move from the motorcycle to camp.',
    'osah-scout-tank-bag-6l': 'The Scout puts 6L of quick-access storage above the tank. Its compact body and strap mounting suit riders who want essentials close without a larger touring bag.',
    'osah-6l-adv-crash-bar-tail-bag': 'A versatile 6L bag for a crash bar or tail section. It carries small tools and ride essentials in a compact package, with black and green photos available to compare.',
    'osah-outrider-hydration-bag': 'The Outrider is a 13L riding pack with a 2L hydration bladder. It keeps water and small gear within reach when stops are far apart.',
    'osah-stretch-straps': 'Secure a changing luggage load with flexible OSAH stretch straps. They are a simple addition to a touring setup when bags need extra restraint.',
    'osah-10l-drypak': 'A 10L dry bag for layers, tools or camp gear. Welded seams and a waterproof PVC shell help keep the contents protected through wet rides.',
    'osah-20l-drypak': 'A 20L dry bag for bulkier touring essentials. Its waterproof PVC construction and welded seams are designed for weather-exposed luggage.',
    'ilm-magnetic-tank-bag': 'Keep ride essentials above the tank with an ILM bag that uses magnets and straps for mounting. It can be taken off the bike with the included shoulder strap.',
    'ilm-motorcycle-adventure-backpack': 'A riding backpack with a supportive waist harness and room for everyday trail essentials. Its stable fit suits motorcycle trips and active days away from the bike.',
    'ilm-balaclava-fm02': 'A light layer under the helmet for wind, dust and sun exposure. The FM02 also helps keep sweat and hair oils away from the helmet lining.',
    'rhinowalk-multifunctional-vest': 'Wear quick-access storage without a full backpack. This Rhinowalk vest combines pockets, adjustable fit and a breathable back for rides and outdoor use.',
    'mjw-6l-crash-bar-bag': 'A compact 6L bag for tools and quick-access gear on an adventure motorcycle. Its weather-resistant construction helps protect contents in changing conditions.',
}

NEW_FEATURES = {
    'kp101ep01-knee-elbow-guard': ['Ergonomic shells shaped for knee and elbow coverage', 'Padded contact areas for a more comfortable fit', 'CE Level 2 certification stated in the workbook'],
    'kp16ep16-mx-knee-elbow-guard': ['Three-section knee design moves with the leg', 'Impact-resistant PC middle shell', 'Guards supplied for knee and elbow protection'],
    'wt01-motorcycle-lumbar-support': ['High-density PP support shell helps spread pressure', 'Breathable panels improve comfort during longer rides', 'Adjustable support around the lower back'],
    'mh01-traillock-pro-phone-mount': ['Vibration-damped phone support', 'Keeps navigation visible at the handlebar', 'Secure grip for a phone on the move'],
    'mh02-traillock-x-pro-phone-camera-mount': ['Phone and action camera mounting in one unit', 'Vibration-damped support', 'Keeps both devices accessible on the ride'],
    'osah-edge-pro-40l-duffel-bag': ['40L storage for touring gear', 'Carry handles for moving the bag off the motorcycle', 'Durable exterior made for outdoor travel'],
    'osah-scout-tank-bag-6l': ['Compact 6L tank-top storage', 'Clipped lid for quick access', 'Strap mounting for a range of motorcycles'],
    'osah-6l-adv-crash-bar-tail-bag': ['6L space for tools and ride essentials', 'Mounts at a crash bar or tail section', 'Black and green variants pictured'],
    'osah-outrider-hydration-bag': ['13L pack with an included 2L bladder', 'Water access while riding', 'Organized space for small trail essentials'],
    'osah-stretch-straps': ['Flexible straps adapt to different luggage loads', 'Quick way to secure extra gear', 'Useful with touring bags and dry packs'],
    'osah-10l-drypak': ['500D PVC waterproof fabric', 'Watertight welded seams', 'Secure buckle closure'],
    'osah-20l-drypak': ['500D PVC waterproof fabric', 'Watertight welded seams', 'Extra 20L capacity for larger loads'],
    'ilm-magnetic-tank-bag': ['Magnet and strap mounting options', 'Four short straps and a shoulder strap listed', 'Accessible storage above the fuel tank'],
    'ilm-motorcycle-adventure-backpack': ['Waist harness helps distribute pack weight', 'Stable fit for riding and walking', 'Designed for motorcycle and trail use'],
    'ilm-balaclava-fm02': ['Helps shield from wind, dust and sun', 'Keeps the helmet lining cleaner', 'Lightweight layer under a helmet'],
    'rhinowalk-multifunctional-vest': ['Multiple pockets for accessible storage', 'Adjustable vest fit', 'Breathable back support'],
    'mjw-6l-crash-bar-bag': ['Compact 6L utility storage', 'Weather-resistant bag construction', 'Grey and black variants pictured'],
}


def story(product):
    return STORIES.get(product['id']) or NEW_STORIES.get(product['id']) or f"Explore {product['name']} for your next ride. Contact Sherpa Quest Nepal for the details that matter to your setup."


def feature_points(product):
    if product['id'] in NEW_FEATURES:
        return NEW_FEATURES[product['id']]
    text = product.get('description', '').lower()
    candidates = [
        ('waterproof liner', 'Removable waterproof liner helps protect packed gear'),
        ('roll-top', 'Roll-top closure helps seal luggage against weather'),
        ('quick-release', 'Quick-release design makes mounting and removal easier'),
        ('ventilation', 'Ventilation helps manage heat during a ride'),
        ('washable', 'Washable interior is easier to keep fresh'),
        ('touchscreen', 'Touchscreen compatibility lets you use a device without removing gloves'),
        ('molle', 'MOLLE attachments add flexible storage options'),
        ('hydration', 'Hydration support keeps water close at hand'),
        ('bluetooth', 'Bluetooth support helps riders stay connected'),
        ('reflective', 'Reflective details improve visibility in low light'),
        ('armor', 'Protective armor supports riding use'),
    ]
    points = [label for token, label in candidates if token in text][:4]
    return points or [story(product)]


def feature_rows(product):
    source = f"{product['name']} {product.get('description', '')}"
    lower = source.lower()
    rows = [('Brand', 'Not specified' if product['brand'] == 'UNBRANDED' else product['brand']), ('Gear type', product['category'])]
    model = re.search(r'\b(?:KP\d+EP\d+|WT\d+|MH\d+)\b', product['name'], re.I)
    if model:
        rows.append(('Model', model.group(0)))
    capacity = re.search(r'\b(\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?)\s*(?:l|ltr|litres?)\b', product['name'], re.I)
    if not capacity and product['id'] == 'osah-outrider-hydration-bag':
        capacity = re.search(r'\b13\s*l\b', source, re.I)
    if capacity:
        rows.append(('Capacity', (capacity.group(1).replace(' ', '') if capacity.lastindex else '13') + ' L'))

    materials = []
    for pattern, value in [
        (r'\b(?:genuine )?cow(?:hide| leather)\b', 'Cow leather'),
        (r'\bgoat(?:skin| skin)\b', 'Goatskin leather'),
        (r'\bgenuine leather\b', 'Genuine leather'),
        (r'\babs shell\b', 'ABS shell'),
        (r'\b(?:600d|1680d)\s*(?:oxford|polyester)\b', 'Reinforced textile shell'),
        (r'\bcordura\b', 'Cordura fabric'),
        (r'\bpvc\b', 'PVC outer'),
        (r'\breinforced webbing\b', 'Reinforced webbing'),
    ]:
        if re.search(pattern, lower) and value not in materials:
            materials.append(value)
    if materials:
        if 'Cow leather' in materials and 'Genuine leather' in materials:
            materials.remove('Genuine leather')
        rows.append(('Construction', ', '.join(materials[:2])))

    safety = []
    if re.search(r'\bdot\b', lower): safety.append('DOT')
    if re.search(r'\bece(?:\s*22\.06)?\b', lower): safety.append('ECE' + (' 22.06' if '22.06' in lower else ''))
    if re.search(r'ce[ -]*(?:level|lvl)\s*2', lower): safety.append('CE Level 2')
    elif re.search(r'ce[ -]*(?:level|lvl)\s*1', lower): safety.append('CE Level 1')
    if safety:
        rows.append(('Certification', ', '.join(safety)))
    elif product['category'] in ('Gloves', 'Boots', 'Riding jackets'):
        protection = []
        for token, text in [('knuckle', 'Knuckle'), ('ankle', 'Ankle'), ('shin', 'Shin'), ('elbow', 'Elbow'), ('shoulder', 'Shoulder')]:
            if token in lower: protection.append(text)
        if protection: rows.append(('Protection areas', ', '.join(protection[:3])))

    weather = None
    if 'ipx6' in lower: weather = 'IPX6 waterproof rating'
    elif 'ip67' in lower: weather = 'IP67 water protection'
    elif re.search(r'10,?000\+?\s*mm', lower): weather = '10,000 mm waterproof rating'
    elif 'waterproof liner' in lower or 'waterproof inner liner' in lower: weather = 'Removable waterproof liner'
    elif 'waterproof' in lower: weather = 'Waterproof construction'
    if weather: rows.append(('Weather protection', weather))

    if product['category'] == 'Phone holders':
        rows.append(('Mount type', 'Phone and action camera' if product['id'].startswith('mh02') else 'Phone'))
        if 'vibration' in lower: rows.append(('Damping', 'Vibration-damped'))
    if product['id'] == 'osah-outrider-hydration-bag':
        rows.append(('Hydration bladder', '2 L included'))

    details = []
    for token, phrase in [
        ('quick-release', 'Quick-release system'), ('roll-top', 'Roll-top closure'),
        ('dual visor', 'Dual visor'), ('removable liner', 'Removable liner'),
        ('mesh ventilation', 'Mesh ventilation'), ('perforated', 'Perforated airflow'),
        ('molle', 'MOLLE compatible'), ('touchscreen', 'Touchscreen compatible'),
        ('bluetooth 5.0', 'Bluetooth 5.0'), ('hydration bladder', 'Hydration bladder'),
    ]:
        if token in lower: details.append(phrase)
    if details: rows.append(('Ride features', ', '.join(details[:3])))
    if product['category'] == 'Intercom':
        riders = re.search(r'\b(?:up to )?(\d+)\s*(?:riders?|people|persons?)\b', lower)
        if riders: rows.append(('Group connection', f"Up to {riders.group(1)} riders"))
    return rows[:7]


SIZE_AND_COLOR = {
    'ilm-606v-dual-sports-helmets': (['M','L'], ['Red/Grey','Matte Black']),
    'ilm-ws-902-dual-sports-helmet': (['M','L'], ['Blue/White','Matte Black']),
    'ilm-mf-568-full-face-helmet': (['M','L'], ['Red/Blue']),
    'ilm-129-helmet': (['M','L'], ['Matte Black','Gloss White']),
    'ilm-902l-modular-helmet': (['M'], ['Gloss Black','Red/Black']),
    'ilm-mf-509-full-face': (['M','L','XL'], ['Gloss Black','Gloss White']),
    'ilm-mf-567-cobra-camelion-helmet': (['M','L','XL'], ['Cobra Chameleon Purple']),
    'ilm-z-501-helmet': (['M','L','XL'], ['Armor Red']),
    'ilm-jk-313-helmet': (['M','L'], ['Matte Black','Gloss Black','Gold/Black']),
    'ilm-mf-510-helmet': ([], ['Sky Grey']),
    'feher-ventilated-breathable-sj2311-riding-jacket-aeroflow': ([], ['Black']),
    'feher-jk-033a-terrain-all-season-2-layer-motor-cycle-riding-jacket': ([], ['Black']),
    'feher-jk-063a-trailguard-3-in-1-all-season-motor-cycle-riding-jacket': ([], ['Black','White']),
    'feher-jk059-storm-x': ([], ['Grey','Black','Blue']),
    'feher-jk-061-rally-x-3-layer-all-season-motorcycle-touring-jacket': ([], ['Grey']),
    'ilm-adventure-riding-jacket': ([], ['Black','Red','White']),
    'alien-monter-howl-classic-glove': ([], ['Black','Red']),
    'alien-monster-howl-fabric-glove': ([], ['Red','Camouflage']),
    'alien-monster-preadator-evolution': ([], ['White','Green']),
    'alien-monster-ultimate-energy': ([], ['Black','Brown']),
    'alien-monster-mountain-breeze': ([], ['Black','White']),
    'alien-monster-ant-king': ([], ['Black','White']),
    'ilm-igoat-skin-leather-gloves': ([], ['Black']),
    'arcx-l60612-urban-guard': (['39','41','42','43','44'], []),
    'arcx-l54947-ironride': (['40','41','42','43','44'], []),
    'arcx-l60024-lunar': (['41','42','43','44'], []),
    'arcx-l60746-aircore': (['40','41','42','43','44'], []),
    'ilm-mx3a-enduro': (['42','43'], []),
    'osah-6l-adv-crash-bar-tail-bag': ([], ['Black','Green']),
    'mjw-6l-crash-bar-bag': ([], ['Grey','Black']),
    'osah-10l-drypak': ([], ['Blue','Olive']),
    'osah-20l-drypak': ([], ['Blue','Olive']),
    'osah-edge-pro-40l-duffel-bag': ([], ['Black']),
    'osah-scout-tank-bag-6l': ([], ['Black']),
    'osah-outrider-hydration-bag': ([], ['Black']),
    'ilm-magnetic-tank-bag': ([], ['Black']),
    'ilm-motorcycle-adventure-backpack': ([], ['Black']),
    'ilm-balaclava-fm02': ([], ['Black']),
    'rhinowalk-multifunctional-vest': ([], ['Black']),
}

COLOR_PREVIEWS = {
    'ilm-606v-dual-sports-helmets': {'Matte Black':'black-01.jpg'},
    'ilm-ws-902-dual-sports-helmet': {'Blue/White':'blue-white-01.jpg','Matte Black':'matte-black-16.jpg'},
    'ilm-mf-568-full-face-helmet': {'Red/Blue':'red-blue-01.jpg'},
    'ilm-129-helmet': {'Matte Black':'matte-black-01.jpg','Gloss White':'gloss-white-01.jpg'},
    'ilm-902l-modular-helmet': {'Gloss Black':'gloss-black-01.jpg'},
    'ilm-mf-509-full-face': {'Gloss Black':'gloss-black-01.jpg','Gloss White':'gloss-white-01.jpg'},
    'ilm-mf-567-cobra-camelion-helmet': {'Cobra Chameleon Purple':'cobra-camelion-01.jpg'},
    'ilm-z-501-helmet': {'Armor Red':'armor-red-01.jpg'},
    'ilm-mf-510-helmet': {'Sky Grey':'sky-grey-01.jpg'},
    'alien-monster-preadator-evolution': {'White':'sand-gloves.png','Green':'olive-gloves.png'},
    'osah-6l-adv-crash-bar-tail-bag': {'Black':'black-01.jpg','Green':'green-01.jpg'},
    'mjw-6l-crash-bar-bag': {'Grey':'grey-01.jpg','Black':'black-01.jpg'},
}

SWATCHES = {
    'Black':'#1a1a1c','Matte Black':'#242326','Gloss Black':'#080809',
    'White':'#f5f3f1','Gloss White':'#fff','Red':'#ba1427','Armor Red':'#b3192c',
    'Grey':'#77787d','Sky Grey':'#abb4bd','Blue':'#2463b7','Green':'#6d735d',
    'Brown':'#8a5c3e','Olive':'#6f7656','Red/Grey':'linear-gradient(135deg,#b51528 50%,#838388 50%)',
    'Blue/White':'linear-gradient(135deg,#2565be 50%,#f7f7f7 50%)',
    'Red/Blue':'linear-gradient(135deg,#b51528 50%,#245eb3 50%)',
    'Red/Black':'linear-gradient(135deg,#b51528 50%,#1b1b1d 50%)',
    'Gold/Black':'linear-gradient(135deg,#b5954a 50%,#1b1b1d 50%)',
    'Cobra Chameleon Purple':'linear-gradient(135deg,#4c4968 40%,#8e477c 70%,#1b1b1d 70%)',
    'Camouflage':'linear-gradient(135deg,#626447 33%,#353a30 33% 67%,#a38b67 67%)',
}


def options_for(product):
    return SIZE_AND_COLOR.get(product['id'], ([], []))


def color_preview(product, color):
    name = COLOR_PREVIEWS.get(product['id'], {}).get(color)
    if name:
        return f"assets/products/{product['id']}/{name}"
    sizes, colors = options_for(product)
    return product['image'] if len(colors) == 1 else None
