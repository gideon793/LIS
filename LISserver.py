import socket
from hl7apy.core import Message, Segment, Field
from hl7apy.parser import parse_message
import psycopg2
from multiprocessing import Process
import sys
import hemat_dictionary


class server:

    def listen(self):
        print('connected')
        self.c, self.addr = self.s.accept()
        self.message = self.c.recv(8192)
        self.parsed_message = parse_message(self.message.decode(), find_groups=False)
        self.message_type = self.parsed_message.msh.msh_9.value
        self.checkmsg()

    def bclisten(self):
        print('connected')
        self.c, self.addr = self.s.accept()
        self.message = self.c.recv(8192)
        self.parsed_message = parse_message(self.message.decode(), find_groups=False)
        self.message_type = self.parsed_message.msh.msh_9.value
        self.bccheckmsg()

    def checkmsg(self):
        if self.message_type.startswith('ORU'):
            print('ORU-HM')
            self.orumessage()
        if self.message_type.startswith('ORM'):
            print('ORM-HM')
            self.orrmessage()

    def bccheckmsg(self):
        if self.message_type.startswith('ORU'):
            print('ORU-BC')
            self.bcorumessage()
        if self.message_type.startswith('QRY'):
            print('QRY-BC')
            self.bcqrymessage()


    def orumessage(self):
        self.m = Message("ACK")
        self.m.add_segment('MSA')
        self.control_id = self.parsed_message.msh.msh_10.value
        self.m.msh.msh_3.value = 'LIS Server'
        self.m.msh.msh_4.value = 'SAN-KER'
        self.m.msh.msh_9.value = 'ACK^R01'
        self.m.msh.msh_10.value = self.control_id
        self.m.msh.msh_11.value = 'P'
        self.m.msh.msh_12.value = '2.3.1'
        self.m.msa.msa_1.value = 'AA'
        self.m.msa.msa_2.value = self.control_id
        self.se = bytes(self.m.to_mllp(), 'utf-8')
        self.c.sendall(self.se)
        self.labno = self.parsed_message.obr.obr_3.value
        print(self.labno)
        conn = psycopg2.connect(database="test", user='odoo', password='', host='192.168.2.100', port='5432')
        cursor = conn.cursor()
        cursor.execute("select id from public.labconnect_test where labno = %s;", (self.labno,))
        self.labno_id = cursor.fetchone()
        results = []
        for idx, obx in enumerate(self.parsed_message.OBX):
            self.testname = self.parsed_message.OBX[idx].OBX_3.value
            self.testresult = self.parsed_message.OBX[idx].OBX_5.value
            self.parsed_testname = {}
            if self.testname in (
                    '6690-2^WBC^LN', '706-2^BAS%^LN', '770-8^NEU%^LN', '713-8^EOS%^LN', '736-9^LYM%^LN',
                    '5905-5^MON%^LN', '718-7^HGB^LN', '787-2^MCV^LN', '785-6^MCH^LN', '786-4^MCHC^LN',
                    '788-0^RDW-CV^LN', '21000-5^RDW-SD^LN', '4544-3^HCT^', '777-3^PLT^LN'):
                self.parsed_testname = list(hemat_dictionary.parsed_name[self.testname])
                self.parsed_testname.append(self.testresult)
                self.parsed_testname.append(self.labno)
                self.parsed_testname.append(self.labno_id)
                self.final_testname = tuple(self.parsed_testname)
                results.append(self.final_testname)
            if self.testname in (
                    '12011^WBC Abnormal^99MRC', '34165-1^Imm Granulocytes?^LN', '15192-8^Atypical Lymphs?^LN',
                    '12013^RBC Abnormal distribution^99MRC', '12014^Anemia^99MRC', '12015^HGB Interfere^99MRC',
                    '12016^PLT Abnormal Distribution^99MRC'):
                self.parsed_testname = 'Abnormal Flag'
                flag = {'12011^WBC Abnormal^99MRC': 'Abnormal WBC',
                        '34165-1^Imm Granulocytes?^LN': 'Immature Granulocyte',
                        '15192-8^Atypical Lymphs?^LN': 'Atypical Lymphocytes',
                        '12013^RBC Abnormal distribution^99MRC': 'Abnormal RBC Distribution',
                        '12014^Anemia^99MRC': 'Anemia',
                        '12015^HGB Interfere^99MRC': 'Haemoglobin abnormality or interference',
                        '12016^PLT Abnormal Distribution^99MRC': 'Abnormal Platelet Distribution'}
                for key, value in flag:
                    if self.testname == value:
                        self.parsed_testvalue = key
                cursor.execute("insert into public.labconnect_labconnect (labno, testname, value) values (%s, %s, %s);",
                               (self.labno, self.parsed_testname, self.parsed_testvalue,))
        print(results)
        final_results = sorted(results, key=lambda x: x[1])
        final_result = []
        for each in final_results:
            final_result.append(each[:1] + each[2:])
        cursor.executemany(
            "insert into public.labconnect_labconnect (testname, unit, range, value, labno, onetoconnect) values (%s, %s, %s, %s, %s, %s)",
            final_results)
        conn.commit()
        cursor.close()
        conn.close()

    def bcorumessage(self):
        self.m = Message("ACK")
        self.m.add_segment('MSA')
        self.control_id = self.parsed_message.msh.msh_10.value
        self.m.msh.msh_3.value = 'LIS Server'
        self.m.msh.msh_4.value = 'SAN-KER'
        self.m.msh.msh_9.value = 'ACK^R01'
        self.m.msh.msh_10.value = self.control_id
        self.m.msh.msh_11.value = 'P'
        self.m.msh.msh_12.value = '2.3.1'
        self.m.msa.msa_1.value = 'AA'
        self.m.msa.msa_2.value = self.control_id
        self.se = bytes(self.m.to_mllp(), 'utf-8')
        self.c.sendall(self.se)
        self.labno = self.parsed_message.obr.obr_3.value
        print(self.labno)
        conn = psycopg2.connect(database="SAN-KER", user='odoo', password='', host='192.168.2.100', port='5432')
        cursor = conn.cursor()
        cursor.execute("select id from public.labconnect_test where labno = %s;", (self.labno,))
        self.labno_id = cursor.fetchone()
        results = []
        for idx, obx in enumerate(self.parsed_message.OBX):
            self.testname = self.parsed_message.OBX[idx].OBX_3.value
            self.testresult = self.parsed_message.OBX[idx].OBX_5.value
            self.parsed_testname = {}
            if self.testname in (
                    '6690-2^WBC^LN', '706-2^BAS%^LN', '770-8^NEU%^LN', '713-8^EOS%^LN', '736-9^LYM%^LN',
                    '5905-5^MON%^LN', '718-7^HGB^LN', '787-2^MCV^LN', '785-6^MCH^LN', '786-4^MCHC^LN',
                    '788-0^RDW-CV^LN', '21000-5^RDW-SD^LN', '4544-3^HCT^', '777-3^PLT^LN'):
                self.parsed_testname = list(hemat_dictionary.parsed_name[self.testname])
                self.parsed_testname.append(self.testresult)
                self.parsed_testname.append(self.labno)
                self.parsed_testname.append(self.labno_id)
                self.final_testname = tuple(self.parsed_testname)
                results.append(self.final_testname)
            if self.testname in (
                    '12011^WBC Abnormal^99MRC', '34165-1^Imm Granulocytes?^LN', '15192-8^Atypical Lymphs?^LN',
                    '12013^RBC Abnormal distribution^99MRC', '12014^Anemia^99MRC', '12015^HGB Interfere^99MRC',
                    '12016^PLT Abnormal Distribution^99MRC'):
                self.parsed_testname = 'Abnormal Flag'
                flag = {'12011^WBC Abnormal^99MRC': 'Abnormal WBC',
                        '34165-1^Imm Granulocytes?^LN': 'Immature Granulocyte',
                        '15192-8^Atypical Lymphs?^LN': 'Atypical Lymphocytes',
                        '12013^RBC Abnormal distribution^99MRC': 'Abnormal RBC Distribution',
                        '12014^Anemia^99MRC': 'Anemia',
                        '12015^HGB Interfere^99MRC': 'Haemoglobin abnormality or interference',
                        '12016^PLT Abnormal Distribution^99MRC': 'Abnormal Platelet Distribution'}
                for key, value in flag:
                    if self.testname == value:
                        self.parsed_testvalue = key
                cursor.execute("insert into public.labconnect_labconnect (labno, testname, value) values (%s, %s, %s);",
                               (self.labno, self.parsed_testname, self.parsed_testvalue,))
        print(results)
        final_results = sorted(results, key=lambda x: x[1])
        final_result = []
        for each in final_results:
            final_result.append(each[:1] + each[2:])
        cursor.executemany(
            "insert into public.labconnect_labconnect (testname, unit, range, value, labno, onetoconnect) values (%s, %s, %s, %s, %s, %s)",
            final_results)
        conn.commit()
        cursor.close()
        conn.close()



    def orrmessage(self):
        self.control_id = self.parsed_message.msh.msh_10.value
        self.sample_id = self.parsed_message.orc.orc_2.value
        self.labno = self.parsed_message.obr.obr_3.value
        conn = psycopg2.connect(database="test", user='odoo', password='', host='127.0.0.1', port='5432')
        cursor = conn.cursor()
        cursor.execute("select id, type from public.labconnect_test where labno = %s;", (self.sample_id,))
        self.labno_id = cursor.fetchone()
        self.labno_id_id = self.labno_id[1]
        self.labno_id_type = self.labno_id[2]
        cursor.execute("SELECT name, registration, dob, gender FROM public.labconnect_test WHERE id =%s; ",
                       (self.labno_id_id,))
        self.patient_details = cursor.fetchone()
        self.patient_firstname = self.patient_details[1].strip().split()[0]
        self.patient_lastname = self.patient_details[1].strip().split()[-1]
        self.patient_registration = self.patient_details[2]
        self.patient_dob = self.patient_details[3]
        self.patient_gender = self.patient_details[4]
        self.m = Message("ORR^O02")
        self.m.add_segment('MSA')
        self.m.add_segment('PID')
        self.m.add_segment('PV1')
        self.m.add_segment('ORC')
        self.m.add_segment('OBR')
        self.m.add_segment('OBX')
        self.m.msh.msh_3.value = 'LIS Server'
        self.m.msh.msh_4.value = 'SAN-KER'
        self.m.msh.msh_9.value = 'ORR^O02'
        self.m.msh.msh_10.value = self.control_id
        self.m.msh.msh_11.value = 'P'
        self.m.msh.msh_12.value = '2.3.1'
        self.m.msa.msa_1.value = 'AA'
        self.m.msa.msa_2.value = self.control_id
        self.m.pid.pid_1.value = '1'
        self.m.pid.pid_3.value = '%s^^^^MR' % (self.patient_registration)
        self.m.pid.pid_5.value = '%s^%s' % (self.patient_lastname, self.patient_firstname)
        self.m.pid.pid_7.value = self.patient_dob
        self.m.pid.pid_8.value = self.patient_gender
        self.m.pv1.pv1_1.value = '1'
        self.m.pv1.pv1_3.value = self.labno_id_type
        self.m.orc.orc_1.value = 'AF'
        self.m.orc.orc_2.value = self.labno
        self.m.obr.obr_1.value = 1
        self.m.obr.obr_2.value = self.labno
        self.m.obr.obr_4.value = '00001^Automated Count^99MRC'
        print(self.labno)
        cursor.close()
        conn.close()
        self.se = bytes(self.m.to_mllp(), 'utf-8')
        self.c.sendall(self.se)

    def hematologysocket(self):
        global socket_process
        socket_process += 1
        while socket_process < sys.maxsize:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.s.bind(('', 10001))
                print("socket bound to 10001")
                self.s.listen(5)
                print("socket is listening")
                while True:
                    self.listen()
            except socket.error as e:
                print('error')
                print(e)

    def biochemistrysocket(self):
        global socket_process
        socket_process += 1
        while socket_process < sys.maxsize:
            try:
                self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.c.bind(('', 10002))
                print("socket bound to 10002" )
                self.c.listen(5)
                print("socket is listening")
                while True:
                    self.bclisten()
            except socket.error as e:
                print('error')
                print(e)



socket_process = 0

if __name__ == '__main__':
    p1 = Process(target=server().hematologysocket)
    p1.start()
    p2= Process(target=server().biochemistrysocket)
