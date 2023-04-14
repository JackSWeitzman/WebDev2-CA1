CREATE TABLE users
(
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    admin BIT
);

CREATE TABLE active
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    body_part TEXT NOT NULL,
    affliction TEXT NOT NULL,
    health INTEGER
);

CREATE TABLE afflictions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    body_part TEXT NOT NULL,
    affliction TEXT NOT NULL,
    debuff TEXT
);

CREATE TABLE body_part_health
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    body_part TEXT NOT NULL,
    body_part_health_total INTEGER NOT NULL,
    body_part_health_active INTEGER NOT NULL
);


INSERT INTO afflictions (body_part, affliction, debuff)
VALUES  ("Whole Body","Paralysis","Your body no longer respond to your commands, you cannot move more than your eyes and face."),
        ("Neck","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Thorax","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Stomach","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Groin","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Left Upper Arm","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Right Upper Arm","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Left Lower Arm","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Right Lower Arm","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Left Hand","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Right Hand","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Left Upper Leg","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Right Upper Leg","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Left Lower Leg","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Right Lower Leg","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Left Foot","Paralysis","This body part no longer responds to your commands, you cannot control this body part."),
        ("Right Foot","Paralysis","This body part no longer responds to your commands, you cannot control this body part.");