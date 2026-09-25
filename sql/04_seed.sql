-- Sample data: 3 stores, 8 employees, 4 doctors, 10 patients, 15 medicines.
-- Medicine dates are relative to today so the demo always has fresh stock,
-- plus two expired lines (Ogen, Rantac) to show the expiry check.

BEGIN;

INSERT INTO pharmacy (store_id, store_name, address, city, state, pincode) VALUES
    (1,'PESUMEDcare MysoreRoad','Ring road banshankari','bengaluru','Karnataka','560081'),
    (2,'PESUMEDcare HAL','indranagar','bengaluru','Karnataka','560025'),
    (3,'PESUMEDcare PESIMSR','NH 219','kuppam','Andhra Pradesh','517425');

INSERT INTO employee (eid, emp_name, address, sex, salary, contact, store_id) VALUES
    (1001,'Ramesh R','no.23,KR Puram,bengaluru','Male',8000,'9435673215',1),
    (1003,'Suresh M','no.24,indranagar,bengaluru','Male',7000,'9435563287',1),
    (1002,'Angelina S','no.26,Shanthinagar,bengaluru','Female',6000,'9435673256',2),
    (1004,'Rupesh D','no.28,Ramurthynagar,bengaluru','Male',9500,'9435673789',3),
    (1006,'Vishnu G','no.30,Mysore Road,bengaluru','Male',6500,'9235673895',1),
    (1005,'Tushar S','no.72,KR Puram,bengaluru','Male',5500,'9456673215',3),
    (1007,'Ravi kumar S','no.45,banshankari,bengaluru','Male',7000,'9765673715',2),
    (1008,'Suma M','no.54,indranagar,bengaluru','Female',9000,'9735663215',3);

INSERT INTO doctor (doc_id, doc_name, address, contact, hospital) VALUES
    (20178,'Satish H M','no.8,indragar,bengaluru','9735663215','Apollo'),
    (20179,'Singamalai J','no.8,indragar,bengaluru','9735901215','Apollo'),
    (20180,'Roopa V M','no.8,krishnanagar,kuppam','9835690215','Narayana Hrudayalaya'),
    (20181,'Satish H M','no.8,malleshwaram,bengaluru','9035950215','Manipal');

INSERT INTO patient (pid, p_name, address, sex, contact, doc_id, store_id) VALUES
    (3001,'rohan D','no.23,KR Puram,bengaluru','Male','9735787321',20178,1),
    (3002,'Sohan M','no.25,Mysore road,bengaluru','Male','9735673215',20179,1),
    (3003,'Lohith N','no.27,Mysore road,bengaluru','Male','9735573215',20178,1),
    (3004,'Vishnu J','no.56,indranagar,bengaluru','Male','9735663455',20180,2),
    (3005,'Tushar M','no.89,Mysore road,bengaluru','Male','9738963215',20179,2),
    (3006,'Venkatesh S','no.60,KR Puram,bengaluru','Male','9835663215',20179,2),
    (3007,'Savithri S','no.57,jayanagar,bengaluru','Female','9935663215',20181,3),
    (3008,'Sangeetha J','no.43,Mysore road,bengaluru','Female','8735663215',20178,3),
    (3009,'Savitha D','no.10,KR Puram,bengaluru','Female','7735663215',20179,3),
    (3010,'Mahitha S','no.8,indragar,bengaluru','Female','8735563615',20180,3);

INSERT INTO medicine (drug_id, drug_name, mfg_date, exp_date, price, manufacturer) VALUES
    (6071, 'Xanax', current_date - 120, current_date + 200, 6.5, 'A D Pharmaceutical'),
    (6072, 'Zyloprim', current_date - 130, current_date + 220, 7.5, 'A D Pharmaceutical'),
    (6073, 'Panretin gel', current_date - 140, current_date + 240, 60.0, 'A D Pharmaceutical'),
    (6074, 'Zovirax', current_date - 150, current_date + 260, 9.6, 'A D Pharmaceutical'),
    (6075, 'Elavil', current_date - 160, current_date + 25, 13.6, 'A D Pharmaceutical'),
    (6076, 'Hyzaar', current_date - 170, current_date + 300, 20.5, 'A S V Laboratories'),
    (6077, 'Lotrel', current_date - 180, current_date + 320, 17.1, 'A S V Laboratories'),
    (6078, 'Lipitor', current_date - 190, current_date + 340, 15.0, 'A S V Laboratories'),
    (6079, 'Ziac', current_date - 200, current_date + 360, 6.5, 'A D Pharmaceutical'),
    (6080, 'Buspar', current_date - 210, current_date + 380, 7.4, 'A S V Laboratories'),
    (6081, 'Ogen', current_date - 400, current_date - 35, 50.0, 'A S V Laboratories'),
    (6082, 'Hydrochlorothiazide', current_date - 230, current_date + 420, 34.6, 'A S V Laboratories'),
    (6083, 'Vitamin B Complex', current_date - 240, current_date + 440, 5.0, 'A S V Laboratories'),
    (6084, 'Vitamin B-6', current_date - 250, current_date + 460, 3.5, 'A D Pharmaceutical'),
    (6085, 'Rantac', current_date - 400, current_date - 35, 6.4, 'A D Pharmaceutical');

INSERT INTO contains (drug_id, store_id, quantity) VALUES
    (6071,1,1000),
    (6072,1,750),
    (6073,1,600),
    (6074,1,500),
    (6075,1,600),
    (6076,1,800),
    (6078,1,400),
    (6079,1,40),
    (6080,1,300),
    (6075,2,1000),
    (6076,2,450),
    (6078,2,750),
    (6079,2,600),
    (6080,2,150),
    (6081,2,250),
    (6082,2,350),
    (6083,2,100),
    (6084,2,500),
    (6085,2,900),
    (6073,3,1000),
    (6074,3,800),
    (6075,3,900),
    (6076,3,550),
    (6078,3,760),
    (6079,3,900),
    (6080,3,800),
    (6081,3,1000),
    (6082,3,950),
    (6083,3,200),
    (6084,3,700),
    (6085,3,50);

INSERT INTO associated_with (doc_id, store_id) VALUES
    (20178,1),
    (20179,1),
    (20181,1),
    (20178,2),
    (20179,2),
    (20181,2),
    (20180,3),
    (20178,3);

-- historical bills; amount is recomputed from the medicine price
INSERT INTO bill (bill_id, pid, doc_id, drug_id, quantity, amount, store_id, billed_at)
SELECT v.bill_id, v.pid, v.doc_id, v.drug_id, v.quantity, m.price * v.quantity, v.store_id, v.billed_at
  FROM (VALUES
    (500001, 3001, 20178, 6071, 3, 1, now() - interval '30 days'),
    (500002, 3002, 20178, 6072, 4, 1, now() - interval '27 days'),
    (500003, 3003, 20178, 6073, 1, 1, now() - interval '24 days'),
    (500004, 3004, 20178, 6076, 6, 2, now() - interval '21 days'),
    (500005, 3005, 20179, 6076, 5, 2, now() - interval '18 days'),
    (500006, 3006, 20179, 6076, 6, 2, now() - interval '15 days'),
    (500007, 3007, 20180, 6078, 7, 3, now() - interval '12 days'),
    (500008, 3008, 20181, 6079, 7, 3, now() - interval '9 days'),
    (500009, 3009, 20181, 6081, 2, 3, now() - interval '6 days'),
    (500010, 3010, 20179, 6072, 3, 3, now() - interval '3 days')
  ) AS v (bill_id, pid, doc_id, drug_id, quantity, store_id, billed_at)
  JOIN medicine m USING (drug_id);

-- explicit IDs were used above, so move each identity sequence past them
SELECT setval(pg_get_serial_sequence('pharmacy', 'store_id'), (SELECT max(store_id) FROM pharmacy));
SELECT setval(pg_get_serial_sequence('employee', 'eid'), (SELECT max(eid) FROM employee));
SELECT setval(pg_get_serial_sequence('doctor', 'doc_id'), (SELECT max(doc_id) FROM doctor));
SELECT setval(pg_get_serial_sequence('patient', 'pid'), (SELECT max(pid) FROM patient));
SELECT setval(pg_get_serial_sequence('medicine', 'drug_id'), (SELECT max(drug_id) FROM medicine));
SELECT setval(pg_get_serial_sequence('bill', 'bill_id'), (SELECT max(bill_id) FROM bill));

COMMIT;
