# User Segments & Personas -- AI-Native Trade Software

**Scope:** SHK and Elektro trades. Solo, Micro, Small segments in scope. Medium and Large explicitly out.

---

## Segmentation

### In-scope segments

| Segment | Size | Who works there | Current software | Beachhead? |
|---------|------|----------------|-----------------|------------|
| **Solo** (Einzelunternehmer) | 1 person | Meister does everything | Basic cloud ERP | No. Pen+paper works. Low pain, low budget. |
| **Micro** (Kleinstbetrieb) | 2-4 people | Meister + 1-2 Gesellen, no dedicated admin | Mid-tier cloud ERP | **Yes.** Multi-user coordination creates real pain. PLG potential. |
| **Small** (Kleinbetrieb) | 5-12 people | Meister + Gesellen + part-time Burokraft | Full ERP (legacy) | No (initially). High switching cost. Follows Micro. |

### Out-of-scope segments

| Segment | Size | Why out |
|---------|------|---------|
| **Medium** (Mittelbetrieb) | 13-25 people | Configuration complexity. Retaining these whales means exorbitant maintenance spend that complicates the product for everyone else. |
| **Large** (Grossbetrieb) | 25+ people | Department structure, IT person, custom workflows. Enterprise sales motion. Wrong game for a new product. |

**Design principle:** Build modular for adjacent expansion, not configurable for 25-person firms from day one.

---

## Personas

### Solo Segment

#### Thomas, 38 -- Solo Meister (the digital-ready one)

SHK Meister, works alone, mostly Heizungswartung and small bathroom renovations for residential clients in a mid-size town near Kassel. Uses basic cloud ERP on his laptop in the evenings. Technically capable -- he set up his own Google Business profile, answers customer inquiries via WhatsApp.

His real work happens in the customer's kitchen: "Frau Schmidt, the valve is fine for now, but next winter we should replace it -- I'll do it for 400 including parts." That handshake IS the quote. The software's job is to catch up: turn that conversation into a record, an invoice later, a reminder in October.

His pain is the 2-3 hours every evening re-entering what he already agreed on-site. He won't pay more than EUR 60/month because "it's just me."

- **What makes him switch:** Voice memo in the van -> structured quote waiting on his laptop at home. The software follows the conversation, not the other way around.
- **What keeps him on current tool:** It works. It's cheap. Switching means re-entering 3 years of customer data.
- **Design insight:** Manual override isn't an edge case -- it's the default workflow. Thomas changes prices, adds line items, rounds down for good customers. Every quote is a negotiation result, not a catalogue lookup. The software that demands he fill forms before he can deviate loses him instantly.

#### Uwe, 61 -- Solo Meister (the resistor)

SHK Meister near retirement, 30+ years in business. Does heating maintenance for a stable pool of 200 residential customers who call him directly. Uwe's entire business runs on relationships: he knows every boiler in his territory, remembers that Herr Fischer's pipes freeze every January, and adjusts his price because Fischer's wife brought him cake last Christmas. None of this is in the software.

His wife types the formal quotes into the ERP once a week -- a chore he considers pointless because "the customer already said yes on the phone." The idea that he should enter data into a system *before* agreeing a price with the customer is offensive to him. He doesn't have a smartphone capable of running apps. He represents the ~20% of Solo operators who will age out of the market within 5-7 years (succession crisis: 12k+ open SHK positions, ZVSHK).

- **What makes him switch:** Nothing. He retires.
- **What matters:** His successor (or the firm that absorbs his customers) inherits the data. The 200 customer relationships in his head are worth more than anything in the ERP.
- **Design insight:** For Uwe, the software is a tax imposed by DATEV and GoBD. Every interaction with it is overhead that follows, never leads, his actual work. A tool that demanded more input would be worse than what he has.
- **Strategic value:** Thousands of Uwes serve millions of residential customers whose maintenance histories exist only in their heads. When they retire, that data evaporates. A product that captures it during succession captures the customer relationship layer of a multi-billion-euro maintenance market.

---

### Micro Segment (beachhead)

#### Dieter, 44 -- Burokraft (the accidental admin)

Married to Svenja, who runs a 3-person SHK firm. Dieter handles invoices, DATEV, and customer calls from the kitchen table while managing the household. He learned the ERP from YouTube tutorials. He has no IT support and no training budget. When Svenja is on-site, he can't reach her for quote approvals -- so he waits, sometimes until 7pm, sometimes until the next morning. Meanwhile the customer calls back: "Haben Sie das Angebot schon geschickt?" He doesn't know what to say. He prints everything because "what if the computer crashes."

- **What makes him switch:** Something that lets Svenja approve quotes from her phone so he doesn't wait until 7pm. Less printing. Less re-typing.
- **What keeps him on current tool:** He spent 6 months learning it. Starting over feels impossible.
- **Aha moment:** The first time a quote goes from Svenja's voice memo on-site to Dieter's screen to customer inbox in under 10 minutes -- without a single phone call between them. "Svenja hat das Angebot freigegeben" as a push notification while he's cooking dinner. That's when the kitchen-table admin realizes the tool is working *for* him, not *on* him.

#### Ayse, 27 -- Gesellin (the PLG adopter)

Works for a 4-person Elektro firm. The Meister (her boss, 52) does everything in his head and on paper. Ayse fills out time sheets on paper that nobody ever reconciles. She knows modern trade software exists because she follows competitors on Instagram. She's told her boss three times that they're losing money on jobs because they don't track hours properly. The boss says "we've always done it this way." She's considering starting her own firm in 2-3 years. If the software is good enough, she'll take it with her.

- **What makes her push for switching:** Seeing her own data -- "we lost EUR 800 on the Mueller job because we spent 6 hours more than quoted." Evidence that her boss can't argue with.
- **What keeps the firm on paper:** The Meister's inertia. Ayse has no purchasing authority.
- **PLG design constraint:** Ayse is the classic bottom-up adopter. She doesn't buy the software -- she discovers it, uses the free/personal tier to track her own hours, shows the Meister the gap between quoted and actual. The aha moment: the first time the data proves a job lost money. **The product must deliver its first value to the Geselle without the Meister's buy-in.** That's the PLG design constraint. If the product requires a Meister's approval to deliver its first value, adoption stalls at the inertia barrier.

---

### Small Segment

#### Markus, 55 -- Meister/Inhaber (the margin-blind expert)

Runs a 9-person SHK firm in Hannover. Legacy ERP user since 2008. Has a Burokraft (part-time) and 6 Gesellen. Markus does quotes himself because "nobody else understands the pricing." He knows his margins are slipping but can't prove it. He heard about modern competitors but won't switch because "all my data is in the old system." He quotes from memory and experience, not from the system.

- **What makes him switch:** Two things, in sequence. First, proof that his margins are below market: "You're quoting EUR 3,600 for bathroom renovations; firms like yours quote EUR 4,200 and make 26% margin." That's the CL value prop landing directly. But proof alone doesn't overcome inertia. The second trigger: "Your 17 years of data come with you -- every quote, every invoice, every customer, every price point. Day one, the system already knows your business." Full history migration with zero data loss is the key.
- **What keeps him on legacy ERP:** Fear of losing 17 years of history. Custom module configuration. The Burokraft knows the old system, not anything else. The migration promise directly neutralizes the first objection.
- **Key insight:** Markus's historical data isn't just his comfort blanket -- it's CL training data. 500+ completed projects with actuals vs. quotes = the delta signal that powers FirmBenchmark from day one. Every migrated customer arrives with a pre-trained model of their own business. External competitors start cold. This is the structural migration moat.

#### Sandra, 36 -- Meisterin/Inhaberin (the growth-oriented one)

Took over her father's 7-person SHK firm in Rheine two years ago. Inherited the ERP from her father. She added a second Geselle team for Elektro jobs and wants to grow to 12 people. Her problem isn't admin -- it's visibility. She can't see which jobs are profitable, which Geselle teams are faster, or whether her Elektro expansion is working. She'd pay EUR 200/month for a tool that shows her the business, not just the paperwork.

- **What makes her switch:** Dashboard with real margins, team performance, CL benchmarks. "Your Elektro margins are 14%; the platform average is 22% -- here's what top performers do differently."
- **What keeps her on current tool:** It handles the basics. Switching mid-growth feels risky.

---

## Adoption Sequence

1. **Ayse and Sandra** come first -- they're already looking. PLG from below (Ayse) and growth pull from above (Sandra).
2. **Markus** follows because of the zero-loss migration promise. His 17 years of data become day-one intelligence, not a cold start. No external competitor can match this.
3. **Dieter/Svenja** follow Markus once the product is proven in their segment.
4. **Uwe** ages out. Capture his customer relationships through succession tooling -- the data in his head matters more than the data in the ERP.

---

## Prototype Implications

- **Demo firm = Micro segment** (Weber Haustechnik, 4 people: 1 Meister, 2 Gesellen, 1 Burokraft part-time)
- **Three hardcoded users** represent the three roles: Meister Weber, Geselle Hoffmann, Burokraft Yilmaz
- **Role switcher** demonstrates that Ayse sees the job but not the margin
- **Two firm contexts** show the migration story (Markus) and the PLG story (Ayse) in the same prototype
