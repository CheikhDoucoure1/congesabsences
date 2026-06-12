"""
Commande pour peupler la base de données avec les employés PETROSEN.
Usage: python manage.py populate_employes
"""
from django.core.management.base import BaseCommand
from datetime import date
from conges.models import Employe, Departement, TypeConge, SoldeConge


class Command(BaseCommand):
    help = 'Peuple la base avec les employés PETROSEN par département et poste'

    def handle(self, *args, **options):
        self.stdout.write('Création/mise à jour des départements...')
        depts = {}
        for nom, code in [
            ('Direction Générale',                   'DG'),
            ('Direction des Ressources Humaines',    'DRH'),
            ('Direction Exploration & Production',   'DEP'),
            ('Direction Finance & Comptabilité',     'FIN'),
            ('Direction HSE',                        'HSE'),
            ('Direction Juridique & Contrats',       'JUR'),
            ('Direction Systèmes d\'Information',    'DSI'),
            ('Direction Logistique & Approvisionnement', 'LOG'),
        ]:
            d, _ = Departement.objects.get_or_create(code=code, defaults={'nom': nom})
            depts[code] = d

        # Structure : (prenom, nom, email, poste, dept_code, role, manager_ref)
        # manager_ref = clé dans le dict employes créé au fur et à mesure
        structure = [
            # ── Direction Générale ──────────────────────────────────────────
            ('Mouhamadou', 'Ndiaye',  'dg@petrosen.sn',
             'Directeur Général',          'DG',  'admin',   None),
            ('Seydina',    'Diallo',  'dga@petrosen.sn',
             'Directeur Général Adjoint',  'DG',  'admin',   'dg@petrosen.sn'),
            ('Adja',       'Sarr',    'a.sarr@petrosen.sn',
             'Secrétaire de Direction',    'DG',  'employe', 'dg@petrosen.sn'),

            # ── Ressources Humaines ─────────────────────────────────────────
            ('Aissatou',   'Ndiaye',  'drh@petrosen.sn',
             'Directrice des Ressources Humaines', 'DRH', 'rh', 'dga@petrosen.sn'),
            ('Babacar',    'Fall',    'b.fall@petrosen.sn',
             'Responsable Recrutement & Formation', 'DRH', 'manager', 'drh@petrosen.sn'),
            ('Ndeye Fatou','Mbaye',   'nf.mbaye@petrosen.sn',
             'Chargée de Paie',            'DRH', 'employe', 'drh@petrosen.sn'),
            ('Lamine',     'Sy',      'l.sy@petrosen.sn',
             'Assistant RH',               'DRH', 'employe', 'drh@petrosen.sn'),

            # ── Exploration & Production ────────────────────────────────────
            ('Ibrahima',   'Diop',    'i.diop@petrosen.sn',
             'Directeur Exploration & Production', 'DEP', 'manager', 'dga@petrosen.sn'),
            ('Mamadou',    'Sow',     'm.sow@petrosen.sn',
             'Ingénieur Réservoir Senior',  'DEP', 'employe', 'i.diop@petrosen.sn'),
            ('Khady',      'Camara',  'k.camara@petrosen.sn',
             'Ingénieure Géologue',         'DEP', 'employe', 'i.diop@petrosen.sn'),
            ('Modou',      'Thiam',   'm.thiam@petrosen.sn',
             'Ingénieur Forage',            'DEP', 'employe', 'i.diop@petrosen.sn'),
            ('Assane',     'Badji',   'a.badji@petrosen.sn',
             'Technicien Process',          'DEP', 'employe', 'i.diop@petrosen.sn'),
            ('El Hadji',   'Coly',    'eh.coly@petrosen.sn',
             'Technicien Réservoir',        'DEP', 'employe', 'i.diop@petrosen.sn'),

            # ── Finance & Comptabilité ──────────────────────────────────────
            ('Ousmane',    'Kane',    'o.kane@petrosen.sn',
             'Directeur Financier',         'FIN', 'manager', 'dga@petrosen.sn'),
            ('Khadija',    'Sarr',    'k.sarr@petrosen.sn',
             'Contrôleure de Gestion',      'FIN', 'employe', 'o.kane@petrosen.sn'),
            ('Cheikh',     'Diouf',   'c.diouf@petrosen.sn',
             'Comptable Senior',            'FIN', 'employe', 'o.kane@petrosen.sn'),
            ('Rokhaya',    'Faye',    'r.faye@petrosen.sn',
             'Trésorière',                 'FIN', 'employe', 'o.kane@petrosen.sn'),
            ('Alioune',    'Thiaw',   'al.thiaw@petrosen.sn',
             'Analyste Budgétaire',         'FIN', 'employe', 'o.kane@petrosen.sn'),

            # ── HSE ─────────────────────────────────────────────────────────
            ('Pape',       'Gueye',   'p.gueye@petrosen.sn',
             'Directeur HSE',              'HSE', 'manager', 'dga@petrosen.sn'),
            ('Fatou',      'Cissé',   'f.cisse@petrosen.sn',
             'Ingénieure Sécurité',        'HSE', 'employe', 'p.gueye@petrosen.sn'),
            ('Youssoupha', 'Ly',      'y.ly@petrosen.sn',
             'Chargé Environnement',        'HSE', 'employe', 'p.gueye@petrosen.sn'),
            ('Aminata',    'Touré',   'am.toure@petrosen.sn',
             'Agent HSE',                  'HSE', 'employe', 'p.gueye@petrosen.sn'),

            # ── Juridique & Contrats ────────────────────────────────────────
            ('Abdoulaye',  'Konaté',  'ab.konate@petrosen.sn',
             'Directeur Juridique',        'JUR', 'manager', 'dga@petrosen.sn'),
            ('Mariama',    'Ba',      'ma.ba@petrosen.sn',
             'Juriste Senior',             'JUR', 'employe', 'ab.konate@petrosen.sn'),
            ('Serigne',    'Ndoye',   's.ndoye@petrosen.sn',
             'Chargé des Contrats',        'JUR', 'employe', 'ab.konate@petrosen.sn'),

            # ── DSI ─────────────────────────────────────────────────────────
            ('Boubacar',   'Sy',      'bo.sy@petrosen.sn',
             'Directeur des Systèmes d\'Information', 'DSI', 'manager', 'dga@petrosen.sn'),
            ('Landing',    'Badji',   'la.badji@petrosen.sn',
             'Administrateur Systèmes',    'DSI', 'employe', 'bo.sy@petrosen.sn'),
            ('Rama',       'Diallo',  'ra.diallo@petrosen.sn',
             'Développeuse Applicative',   'DSI', 'employe', 'bo.sy@petrosen.sn'),
            ('Cheikh',     'Doucoure','cdoucoure@petrosen.sn',
             'Technicien Réseau',          'DSI', 'employe', 'bo.sy@petrosen.sn'),

            # ── Logistique & Approvisionnement ──────────────────────────────
            ('Mame Diarra','Fall',    'md.fall@petrosen.sn',
             'Directrice Logistique & Approvisionnement', 'LOG', 'manager', 'dga@petrosen.sn'),
            ('Ousmane',    'Fall',    'ou.fall@petrosen.sn',
             'Responsable Approvisionnement', 'LOG', 'employe', 'md.fall@petrosen.sn'),
            ('Saliou',     'Mbaye',   'sa.mbaye@petrosen.sn',
             'Chargé des Achats',          'LOG', 'employe', 'md.fall@petrosen.sn'),
            ('Coumba',     'Ndiaye',  'co.ndiaye@petrosen.sn',
             'Magasinière',               'LOG', 'employe', 'md.fall@petrosen.sn'),
        ]

        self.stdout.write(f'Création de {len(structure)} employés...')
        created_map = {}  # email → instance

        # Premier passage : créer tous les employés sans manager
        for prenom, nom, email, poste, dept_code, role, _ in structure:
            username = email.split('@')[0]
            if not Employe.objects.filter(email=email).exists():
                emp = Employe.objects.create_user(
                    username=username,
                    email=email,
                    password='Petrosen2025!',
                    first_name=prenom,
                    last_name=nom,
                )
                emp.poste = poste
                emp.role = role
                emp.departement = depts[dept_code]
                emp.actif = True
                emp.save()
                created_map[email] = emp
                self.stdout.write(f'  + {prenom} {nom} — {poste}')
            else:
                emp = Employe.objects.get(email=email)
                emp.poste = poste
                emp.role = role
                emp.departement = depts[dept_code]
                emp.actif = True
                emp.save()
                created_map[email] = emp
                self.stdout.write(f'  ~ {prenom} {nom} — mis à jour')

        # Deuxième passage : affecter les managers
        for _, _, email, _, _, _, manager_email in structure:
            if manager_email and manager_email in created_map:
                emp = created_map[email]
                emp.manager = created_map[manager_email]
                emp.save()

        # Initialiser les soldes de congés annuels (24j) pour tous
        self.stdout.write('Initialisation des soldes congés annuels (24j)...')
        annee = date.today().year
        type_annuel = TypeConge.objects.filter(code='annuel').first()
        if type_annuel:
            for emp in created_map.values():
                SoldeConge.objects.get_or_create(
                    employe=emp,
                    type_conge=type_annuel,
                    annee=annee,
                    defaults={'jours_acquis': 24, 'jours_pris': 0}
                )

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ {len(created_map)} employés créés/mis à jour avec succès!\n'
            f'Mot de passe par défaut : Petrosen2025!'
        ))
