-- Mock Data For Tests

INSERT INTO users (email, password, role)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$YKTR53od$3956727084a9d3470d800ca00005a2258bde5affab208eb9ae211c46a28f575d', 'teacher'),
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$db49oioE$95b37dfa834211006b45fddfa03debdca5d2ccf49486bb7e35af144406d51c8a', 'student');
