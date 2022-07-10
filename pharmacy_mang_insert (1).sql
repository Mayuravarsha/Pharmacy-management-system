\c pharmacy_mang

INSERT into PHARMACY values(1,'PESUMEDcare MysoreRoad','Ring road banshankari','bengaluru','Karnataka','560081');
INSERT into PHARMACY values(2,'PESUMEDcare HAL','indranagar','bengaluru','Karnataka','560025');
INSERT into PHARMACY values(3,'PESUMEDcare PESIMSR','NH 219','kuppam','Andhra Pradesh','517425');

INSERT into EMPLOYEE values(1001,'Ramesh R','no.23,KR Puram,bengaluru','Male',8000,'9435673215',1);
INSERT into EMPLOYEE values(1003,'Suresh M','no.24,indranagar,bengaluru','Male',7000,'9435563287',1);
INSERT into EMPLOYEE values(1002,'Angelina S','no.26,Shanthinagar,bengaluru','Female',6000,'9435673256',2);
INSERT into EMPLOYEE values(1004,'Rupesh D','no.28,Ramurthynagar,bengaluru','Male',9500,'9435673789',3);
INSERT into EMPLOYEE values(1006,'Vishnu G','no.30,Mysore Road,bengaluru','Male',6500,'9235673895',1);
INSERT into EMPLOYEE values(1005,'Tushar S','no.72,KR Puram,bengaluru','Male',5500,'9456673215',3);
INSERT into EMPLOYEE values(1007,'Ravi kumar S','no.45,banshankari,bengaluru','Male',7000,'9765673715',2);
INSERT into EMPLOYEE values(1008,'Suma M','no.54,indranagar,bengaluru','Female',9000,'9735663215',3);

INSERT into DOCTOR values(20178,'Satish H M','no.8,indragar,bengaluru','9735663215','Apollo');
INSERT into DOCTOR values(20179,'Singamalai J','no.8,indragar,bengaluru','9735901215','Apollo');
INSERT into DOCTOR values(20180,'Roopa V M','no.8,krishnanagar,kuppam','9835690215','Narayana Hrudayalaya');
INSERT into DOCTOR values(20181,'Satish H M','no.8,malleshwaram,bengaluru','9035950215','Manipal');

INSERT into PATIENT values(3001,'rohan D','no.23,KR Puram,bengaluru','Male','9735787321',20178,1);
INSERT into PATIENT values(3002,'Sohan M','no.25,Mysore road,bengaluru','Male','9735673215',20179,1);
INSERT into PATIENT values(3003,'Lohith N','no.27,Mysore road,bengaluru','Male','9735573215',20178,1);
INSERT into PATIENT values(3004,'Vishnu J','no.56,indranagar,bengaluru','Male','9735663455',20180,2);
INSERT into PATIENT values(3005,'Tushar M','no.89,Mysore road,bengaluru','Male','9738963215',20179,2);
INSERT into PATIENT values(3006,'Venkatesh S','no.60,KR Puram,bengaluru','Male','9835663215',20179,2);
INSERT into PATIENT values(3007,'Savithri S','no.57,jayanagar,bengaluru','Female','9935663215',20181,3);
INSERT into PATIENT values(3008,'Sangeetha J','no.43,Mysore road,bengaluru','Female','8735663215',20178,3);
INSERT into PATIENT values(3009,'Savitha D','no.10,KR Puram,bengaluru','Female','7735663215',20179,3);
INSERT into PATIENT values(3010,'Mahitha S','no.8,indragar,bengaluru','Female','8735563615',20180,3);

INSERT into MEDICINE values(6071,'Xanax','20-06-2020','21-06-2021', 6.5,'A D Phamaceutical');
INSERT into MEDICINE values(6072,'Zyloprim','20-06-2020','21-06-2021', 7.5,'A D Phamaceutical');
INSERT into MEDICINE values(6073,'Panretin gel','20-06-2020','21-06-2021', 60.0,'A D Phamaceutical');
INSERT into MEDICINE values(6074,'Zovirax','20-06-2020','21-06-2021', 9.6,'A D Phamaceutical');
INSERT into MEDICINE values(6075,'Elavil','20-06-2020','21-06-2021', 13.6,'A D Phamaceutical');
INSERT into MEDICINE values(6076,'Hyzaar','20-06-2020','21-06-2021', 20.5,'A S V Laboritries');
INSERT into MEDICINE values(6077,'Lotrel','19-02-2020','20-02-2021', 17.1,'A S V Laboritries');
INSERT into MEDICINE values(6078,'Lipitor','19-02-2020','20-02-2021', 15.0,'A S V Laboritries');
INSERT into MEDICINE values(6079,'Ziac','19-02-2020','20-02-2021', 6.5,'A D Phamaceutical');
INSERT into MEDICINE values(6080,'Buspar','19-02-2020','20-02-2021', 7.4,'A S V Laboritries');
INSERT into MEDICINE values(6081,'Ogen','19-02-2020','20-02-2021', 50.0,'A S V Laboritries');
INSERT into MEDICINE values(6082,'Hydrochlorothiazide','31-07-2020','30-07-2021', 34.6,'A S V Laboritries');
INSERT into MEDICINE values(6083,'Vitamin B Complex','31-07-2020','30-07-2021', 5.0,'A S V Laboritries');
INSERT into MEDICINE values(6084,'Vitamin B-6','31-07-2020','30-07-2021', 3.5,'A D Phamaceutical');
INSERT into MEDICINE values(6085,'Rantac','31-07-2020','30-07-2021', 6.4,'A D Phamaceutical');

INSERT into BILL values(500001,3001,20178,6071,3,22.0,1);
INSERT into BILL values(500002,3002,20178,6072,4,33.0,1);
INSERT into BILL values(500003,3003,20178,6073,1,62.0,1);
INSERT into BILL values(500004,3004,20178,6076,6,126.0,2);
INSERT into BILL values(500005,3005,20179,6076,5,101.0,2);
INSERT into BILL values(500006,3006,20179,6076,6,126.0,2);
INSERT into BILL values(500007,3007,20180,6078,7,109.5,3);
INSERT into BILL values(500008,3008,20181,6079,7,52.6,3);
INSERT into BILL values(500009,3009,20181,6081,2,102.7,3);
INSERT into BILL values(500010,3010,20179,6072,3,26.2,3);

INSERT into contains values(6071,1,1000);
INSERT into contains values(6072,1,750);
INSERT into contains values(6073,1,600);
INSERT into contains values(6074,1,500);
INSERT into contains values(6075,1,600);
INSERT into contains values(6076,1,800);
INSERT into contains values(6078,1,400);
INSERT into contains values(6079,1,40);
INSERT into contains values(6080,1,300);
INSERT into contains values(6075,2,1000);
INSERT into contains values(6076,2,450);
INSERT into contains values(6078,2,750);
INSERT into contains values(6079,2,600);
INSERT into contains values(6080,2,150);
INSERT into contains values(6081,2,250);
INSERT into contains values(6082,2,350);
INSERT into contains values(6083,2,100);
INSERT into contains values(6084,2,500);
INSERT into contains values(6085,2,900);
INSERT into contains values(6073,3,1000);
INSERT into contains values(6074,3,800);
INSERT into contains values(6075,3,900);
INSERT into contains values(6076,3,550);
INSERT into contains values(6078,3,760);
INSERT into contains values(6079,3,900);
INSERT into contains values(6080,3,800);
INSERT into contains values(6081,3,1000);
INSERT into contains values(6082,3,950);
INSERT into contains values(6083,3,200);
INSERT into contains values(6084,3,700);
INSERT into contains values(6085,3,50);


INSERT into Associated_With values(20178,1);
INSERT into Associated_With values(20179,1);
INSERT into Associated_With values(20181,1);
INSERT into Associated_With values(20178,2);
INSERT into Associated_With values(20179,2);
INSERT into Associated_With values(20181,2);
INSERT into Associated_With values(20180,3);
INSERT into Associated_With values(20178,3);

