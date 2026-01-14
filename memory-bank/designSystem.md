# Design System — HelpMe!

## Direzione Creativa

**Estetica organica e umana** che riflette il concetto di aiuto reciproco e community.

### Principi Guida
- **Calore e accoglienza**: Palette terrosa che crea un ambiente invitante
- **Chiarezza**: Tipografia leggibile e gerarchia visiva forte
- **Organicità**: Bordi arrotondati, ombre morbide, layout asimmetrici
- **Semplicità**: No gradienti, emoji limitate, focus sul contenuto

---

## Palette Colori

### Colori Primari
```css
--color-bg: #FBF7F0          /* Background principale - beige chiaro */
--color-surface: #FFFFFF      /* Card e superfici elevate */
--color-primary: #D85A3C      /* Arancio bruciato - CTA e accenti */
--color-primary-dark: #B8442A /* Arancio scuro - hover stati */
```

### Colori Secondari
```css
--color-secondary: #4A6B5C    /* Verde salvia - badge esperti */
--color-accent: #F4A261        /* Arancio chiaro - accenti secondari */
```

### Colori Testo
```css
--color-text: #2C2416         /* Testo principale - marrone scuro */
--color-text-muted: #6B5D4F   /* Testo secondario - marrone medio */
```

### Colori Utility
```css
--color-border: #E8DCC8       /* Bordi e divisori */
```

### Regole d'Uso
- **Background principale**: sempre `--color-bg` per coerenza
- **Card e superfici**: `--color-surface` con bordo `--color-border`
- **CTA primarie**: `--color-primary` (no gradienti)
- **Badge esperti**: `--color-secondary`
- **Avatar**: colori solidi (primary o secondary)
- **NO gradienti**: usare sempre colori solidi

---

## Tipografia

### Font Families
```css
/* Display/Titoli */
font-family: 'Fraunces', serif;

/* Body/Interfaccia */
font-family: 'Work Sans', -apple-system, BlinkMacSystemFont, sans-serif;
```

### Scale Tipografica (modular scale 1.25)
- **Hero h1**: 3.5rem (56px) - Fraunces 800
- **Section h2**: 2.5rem (40px) - Fraunces 700
- **Section h2 (small)**: 2rem (32px) - Fraunces 700
- **Card h3**: 1.5rem (24px) - Fraunces 700
- **Sidebar h3**: 1.25rem (20px) - Fraunces 700
- **Body**: 1rem (16px) - Work Sans 400
- **Body large**: 1.15rem (18.4px) - Work Sans 400
- **Small**: 0.95rem (15.2px) - Work Sans 400/500
- **XSmall**: 0.85rem (13.6px) - Work Sans 400/500

### Pesi Font
- **Work Sans**: 300 (light), 400 (regular), 500 (medium), 600 (semibold)
- **Fraunces**: 700 (bold), 800 (extrabold)

### Line Heights
- Titoli: 1.1 - 1.3
- Body: 1.6 - 1.7
- UI elements: 1.5

### Regole d'Uso
- **Fraunces**: solo per titoli e numeri grandi (statistiche)
- **Work Sans**: tutto il resto (body, UI, form)
- **Letter-spacing**: -0.02em/-0.03em per Fraunces grandi

---

## Spaziatura

### Griglia Base
Basata su **step 8px**

### Spacing Scale
```css
0.25rem = 4px
0.375rem = 6px
0.5rem = 8px
0.625rem = 10px
0.75rem = 12px
0.875rem = 14px
1rem = 16px
1.25rem = 20px
1.5rem = 24px
1.75rem = 28px
2rem = 32px
2.5rem = 40px
3rem = 48px
4rem = 64px
```

### Padding Standard
- **Card piccole**: 1.75rem (28px)
- **Card medie**: 2rem (32px)
- **Section**: 3rem - 4rem (48-64px)
- **Container**: 2rem (32px) laterale

### Gap Standard
- **Elementi inline**: 0.5rem - 0.75rem
- **Card grid**: 1rem - 1.5rem
- **Sezioni layout**: 2rem - 4rem

---

## Border Radius

### Scale
```css
/* Piccolo - tag, badge */
border-radius: 8px - 12px;

/* Medio - card, input */
border-radius: 16px - 20px;

/* Grande - card principali */
border-radius: 20px - 24px;

/* Pill - bottoni */
border-radius: 100px;

/* Avatar */
border-radius: 50%;
```

---

## Ombre

### Shadow System
```css
/* Soft - card elevate */
--shadow-soft: 
  0 8px 24px -4px rgba(44, 36, 22, 0.12), 
  0 4px 8px -2px rgba(44, 36, 22, 0.08);

/* Hover - card interattive */
--shadow-hover: 
  0 12px 32px -6px rgba(44, 36, 22, 0.18),
  0 6px 12px -3px rgba(44, 36, 22, 0.12);

/* Button primary */
box-shadow: 0 2px 8px rgba(216, 90, 60, 0.3);

/* Button primary hover */
box-shadow: 0 4px 12px rgba(216, 90, 60, 0.4);
```

### Regole d'Uso
- Ombre sempre con colore base `rgba(44, 36, 22, ...)` per coerenza
- Layer multipli per profondità naturale
- Aumentare opacità e spread su hover

---

## Componenti UI

### Bottoni

#### Primary Button
```css
background: var(--color-primary);
color: white;
padding: 0.625rem 1.5rem;
border-radius: 100px;
font-weight: 600;
font-size: 0.9rem;
box-shadow: 0 2px 8px rgba(216, 90, 60, 0.3);
```

Hover: 
- `background: var(--color-primary-dark)`
- `transform: translateY(-1px)`
- `box-shadow: 0 4px 12px rgba(216, 90, 60, 0.4)`

#### Outline Button
```css
background: transparent;
color: var(--color-text);
border: 2px solid var(--color-border);
padding: 0.625rem 1.5rem;
border-radius: 100px;
font-weight: 600;
font-size: 0.9rem;
```

Hover:
- `border-color: var(--color-primary)`
- `color: var(--color-primary)`

### Card

#### Card Standard
```css
background: var(--color-surface);
border: 2px solid var(--color-border);
border-radius: 20px;
padding: 2rem;
transition: all 0.3s;
```

#### Card con Bordo Accent
Aggiungere `::before` con:
```css
position: absolute;
top: 0;
left: 0;
width: 4px;
height: 100%;
background: var(--color-primary);
```

### Avatar

#### Avatar Standard
```css
width: 40px;
height: 40px;
border-radius: 50%;
background: var(--color-primary); /* colore solido */
color: white;
font-weight: 600;
font-size: 0.9rem;
```

#### Avatar Expert
```css
width: 44px;
height: 44px;
background: var(--color-secondary); /* colore solido */
```

### Badge

#### Badge Esperto
```css
background: var(--color-secondary);
color: white;
font-size: 0.7rem;
padding: 0.2rem 0.5rem;
border-radius: 8px;
font-weight: 600;
text-transform: uppercase;
letter-spacing: 0.03em;
```

#### Status Badge
```css
padding: 0.375rem 1rem;
border-radius: 12px;
font-size: 0.85rem;
font-weight: 600;
```

Stato Aperto:
```css
background: rgba(74, 107, 92, 0.15);
color: var(--color-secondary);
```

Stato Chiuso/Risolto:
```css
background: rgba(216, 90, 60, 0.15);
color: var(--color-primary);
```

### Tag Categoria

#### Desktop
```css
background: var(--color-bg);
border: 2px solid var(--color-border);
border-radius: 16px;
padding: 1.25rem 1.5rem;
transition: all 0.3s;
```

Hover:
- `border-color: var(--color-primary)`
- `transform: translateY(-2px)`
- `box-shadow: var(--shadow-soft)`

#### In Post (piccolo)
```css
background: var(--color-bg);
border: 1px solid var(--color-border);
padding: 0.375rem 0.875rem;
border-radius: 12px;
font-size: 0.85rem;
font-weight: 500;
```

---

## Icone

### Sistema Icone
**Usare icone SVG inline** con sistema Feather Icons style:
- stroke-width: 2
- stroke-linecap: round
- stroke-linejoin: round
- fill: none
- stroke: currentColor

### Dimensioni
```css
/* Piccole - inline text */
width: 16px;
height: 16px;

/* Medie - UI elements */
width: 18px;
height: 18px;

/* Grandi - feature */
width: 24px;
height: 24px;
```

### Icone Comuni
- **Commenti**: message-square
- **Visualizzazioni**: eye
- **Notifiche**: bell
- **Utente**: user
- **Cerca**: search
- **Chiudi**: x

### Emoji (uso limitato)
**Permesse SOLO per:**
1. Logo HelpMe! (🤝)
2. Icone categorie (👨‍🍳 🌱 💻 🔧 📚 ⚡)

**NON usare emoji per:**
- Statistiche/metriche
- Azioni UI
- Stati
- Decorazioni generali

---

## Animazioni

### Transizioni Standard
```css
transition: all 0.2s ease;   /* Bottoni */
transition: all 0.3s ease;   /* Card, elementi grandi */
```

### Hover Effects
- **Bottoni**: `translateY(-1px)` + shadow increase
- **Card**: `translateY(-2px)` + border color + shadow
- **Links**: color change

### Animazioni di Entrata
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

animation: fadeInUp 0.6s ease-out backwards;
```

Stagger delays:
- Card 1: 0.1s
- Card 2: 0.2s
- Card 3: 0.3s

---

## Layout

### Container Widths
```css
max-width: 1280px;  /* Container principale */
margin: 0 auto;
padding: 0 2rem;
```

### Grid System

#### Posts Layout
```css
display: grid;
grid-template-columns: 1fr 320px;  /* Main + Sidebar */
gap: 2rem;
```

#### Categories Grid
```css
display: grid;
grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
gap: 1rem;
```

### Responsive Breakpoints
```css
/* Mobile */
@media (max-width: 768px)

/* Tablet */
@media (max-width: 1024px)
```

---

## Accessibilità

### Contrasto
- **Testo normale su bg**: minimo 4.5:1 ✓
- **Testo large su bg**: minimo 3:1 ✓
- **Testo su primary**: white su #D85A3C ✓

### Focus States
```css
outline: 2px solid var(--color-primary);
outline-offset: 2px;
```

### Navigazione Tastiera
- Tutti gli elementi interattivi focusabili
- Focus visibile sempre presente
- Tab order logico

---

## Pattern Specifici HelpMe!

### Post Card
- Border 2px solid
- Border-radius 20px
- Padding 2rem
- Hover: bordo primary + translateY(-2px)
- Accent top bar su hover (4px height, primary)

### Expert Badge
- Sempre uppercase
- Verde secondario
- Accanto al nome utente

### Status Post
- Badge arrotondato (12px)
- Background con alpha 0.15
- Testo color saturo

### Category Icon + Text
- Emoji grande (2rem) centrata
- Nome categoria bold sotto
- Count grigio sotto nome

---

## File di Riferimento

- **Demo completo**: `/demo-design.html`
- **Font**: Google Fonts (Fraunces, Work Sans)
- **Icone**: SVG inline stile Feather Icons

---

## Note Implementazione

### CSS Custom Properties
Usare sempre variabili CSS per:
- Colori
- Ombre
- Spacing ripetuto

### Mobile First
- Iniziare sempre da mobile
- Aggiungere complessità su schermi grandi
- Grid che collassa a colonna singola

### Performance
- Font preconnect per Google Fonts
- SVG inline per icone comuni
- Animazioni con transform (GPU accelerated)

---

## Cosa EVITARE

❌ **Gradienti** - usare colori solidi
❌ **Emoji estensive** - solo logo e categorie
❌ **Font generici** - no Inter, Roboto, Arial, system fonts standard
❌ **Purple su white** - palette troppo comune
❌ **Shadow estreme** - mantenere subtili
❌ **Border sottili** - preferire 2px per definizione
❌ **Layout rigidi** - permettere asimmetria organica

---

Ultimo aggiornamento: 14 gennaio 2026
