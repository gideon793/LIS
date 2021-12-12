parsed_name = {'718-7^HGB^LN': ('Haemoglobin', 1, 'g/dL', '12-17 g/dL'),
               '6690-2^WBC^LN': ('Total Count', 2, 'per \u03BCL', '4000-1000 per \u03BCL '),
               '706-2^BAS%^LN': ('Basophils', 6, '%', '3-5%'),
               '770-8^NEU%^LN': ('Neutrophils', 3, '%', '50-70%'),
               '713-8^EOS%^LN': ('Eosinophils', 5, '%', '3-5%'), '736-9^LYM%^LN': ('Lymphocytes', 4, '%', '30-40%'),
               '5905-5^MON%^LN': ('Monocytes', 7, '%', '1-2%'),
               '787-2^MCV^LN': ('MCV', 10, '\u03BCm\u00b3', '70-90 \u03BCm\u00b3'),
               '785-6^MCH^LN': ('MCH', 11, 'pg', '70-100'),
               '786-4^MCHC^LN': ('MCHC', 12, 'g/dL', '50-100g/dL'), '788-0^RDW-CV^LN': ('RDW_CV', 13, '%', '5-10%'),
               '21000-5^RDW-SD^LN': ('RDW_SD', 14, 'fL', '5-10 fL'),
               '4544-3^HCT^LN': ('Hematocrit', 9, '%', '40-60%'),
               '777-3^PLT^LN': ('Platelets', 8, 'per mcL', '150000-450000 per mcL')}

units = {'6690-2^WBC^LN': 'per \u03BCL', '706-2^BAS%^LN': '%', '770-8^NEU%^LN': '%',
         '713-8^EOS%^LN': '%', '736-9^LYM%^LN': '%', '5905-5^MON%^LN': '%',
         '718-7^HGB^LN': 'g/dL', '787-2^MCV^LN': '\u03BCm\u00b3', '785-6^MCH^LN': 'pg',
         '786-4^MCHC^LN': 'g/dL', '788-0^RDW-CV^LN': '%', '21000-5^RDW-SD^LN': 'fL',
         '4544-3^HCT^LN': '%', '777-3^PLT^LN': 'per mcL'}

range = {'6690-2^WBC^LN': '4000-10000', '706-2^BAS%^LN': 'Basophils', '770-8^NEU%^LN': 'Neutrophils',
         '713-8^EOS%^LN': 'Eosinophils', '736-9^LYM%^LN': 'Lymphocytes', '5905-5^MON%^LN': 'Monocytes',
         '7^HGB^LN': 'Haemoglobin', '787-2^MCV^LN': 'MCV', '785-6^MCH^LN': 'MCH',
         '786-4^MCHC^LN': 'MCHC', '788-0^RDW-CV^LN': 'RDW_CV', '21000-5^RDW-SD^LN': 'RDW_SD',
         '4544-3^HCT^LN': 'Hematocrit', '777-3^PLT^LN': 'Platelets'}
print(parsed_name)
parsed_name_sort = sorted(parsed_name.items(), key=lambda x: x[1][1])
print(parsed_name_sort)
