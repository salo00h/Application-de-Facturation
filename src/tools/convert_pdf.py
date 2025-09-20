from pylatex import Document, Section, Command, Tabular, Package, Figure
from pylatex.utils import NoEscape
import os
from const import *

def convert_pdf(id_utilisateur, info_facture, info_entreprise, info_client, table_articles, infos_supplem, devis=1):
    # Détermination du type de document (Devis ou Facture)
    if devis:
        title = "Devis"
    else:
        title = "Facture"
        info_banqu = infos_supplem[3]

    num_title = info_facture[0]
    logo = info_entreprise[5]
    info_pay = infos_supplem[0]
    remarque = infos_supplem[1]
    signature = infos_supplem[2]

    # Création du document LaTeX
    doc = Document()

    # Ajout des packages pour la mise en page
    doc.packages.append(Package('geometry', options=['top=0.5cm', 'bottom=0.5cm', 'left=0.5cm', 'right=0.5cm']))
    doc.packages.append(Package('graphicx'))

    # Ajout des informations de la facture
    if logo:
        with doc.create(Figure(position='h!')) as image:
            image.add_image(logo, width=NoEscape(r'0.2\textwidth'))

    doc.append(Command('begin', 'flushright'))
    doc.append(f"N° {title} : {info_facture[0]}\n")
    doc.append(f"Date {title} : {info_facture[1]}\n")
    doc.append(f"Ref Client : {info_facture[2]}\n")
    doc.append(Command('end', 'flushright'))

    doc.append("# ) Informations de l'entreprise : \n")
    doc.append(f'Nom Entreprise : {info_entreprise[0]}\n')
    doc.append(f'Adresse : {info_entreprise[1]}\n')
    doc.append(f'Mail : {info_entreprise[2]}\n')
    doc.append(f'Tél. Fixe : {info_entreprise[3]}\n')
    doc.append(f'N° SIREN/SIRET : {info_entreprise[4]}\n')

    doc.append("# ) Informations du Client : \n")
    doc.append(f'Nom Client  : {info_client[0]}\n')
    doc.append(f'Prénom Client : {info_client[1]}\n')
    doc.append(f'Adresse : {info_client[2]}\n')
    doc.append(f'Tél. Fixe : {info_client[3]}\n')
    doc.append(f'Tél Mobile : {info_client[4]}\n')

    # Ajout du tableau des articles
    with doc.create(Section('', numbering=False)):
        with doc.create(Tabular('|c|c|c|c|c|c|')) as table:
            table.add_hline()
            table.add_row(('Intervention', 'Prix unitaire', 'Quantité', 'TVA %','Total HT',  'Total TTC'))
            table.add_hline()
            for article in table_articles:
                table.add_row(article )
            table.add_hline()

    if devis:
        # Ajout du total HT et TTC pour le devis
        
        doc.append(Command('begin', 'flushright'))
        doc.append(f'Total HT : {info_pay[0]}\n')
        doc.append(f'Total TTC : {info_pay[1]}\n')
        doc.append(Command('end', 'flushright'))
    else:
        # Ajout du total HT, TTC, remise, solde dû et mode de paiement pour la facture
        
        doc.append(Command('begin', 'flushright'))
        doc.append(f'Total HT : {info_pay[0]}\n')
        doc.append(f'Total TTC : {info_pay[1]}\n')
        doc.append(f'Remise : {info_pay[2]}\n')
        doc.append(f'Montant Payée : {info_pay[4]}\n')
        doc.append(f'Solde Dû : {info_pay[5]}\n')
        doc.append(f'Mode de paiement  : {info_pay[6]}\n')
        doc.append(f"Date d'échange : {info_pay[7]}\n")
        doc.append(Command('end', 'flushright'))

        # Ajout des informations bancaires pour la facture
        
        doc.append(f"Informations Bancaires : \n")
        doc.append(f'Nom Banque : { info_banqu[0]}\n')
        doc.append(f'RIB : { info_banqu[1]}\n')
        doc.append(f'IBAN : { info_banqu[2]}\n')
        doc.append(f'BIC : { info_banqu[3]}\n')
        
        

    # Ajout de la remarque
    with doc.create(Section('Remarque :', numbering=False)):
        
        doc.append(f"{remarque}\n")

    # Ajout de la signature si nécessaire
    if signature == 1:
        doc.append(Command('begin', 'flushright'))
        doc.append('Signature :\n')
        with doc.create(Figure(position='h!')) as image:
            image_singe = os.path.join(DATA_DIR, f"signature_{id_utilisateur}.png")
            image.add_image(image_singe, width=NoEscape(r'0.2\textwidth'))
        doc.append(Command('end', 'flushright'))


    # Chemin complet du fichier PDF à générer
    chemin_pdf = f"DATA/{num_title}_ID_{id_utilisateur}"

    # Vérification de l'existence du fichier PDF et suppression s'il existe
    if os.path.exists(chemin_pdf):
        os.remove(chemin_pdf)

    # Génération du PDF
    doc.generate_pdf(chemin_pdf, clean_tex=True)

    
