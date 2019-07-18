import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='*********', host='127.0.0.1', port=3306)

# Descomente se quiser desfazer o banco...
conn.cursor().execute("DROP DATABASE `jogoteca`;")
conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `jogoteca` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `jogoteca`;
    CREATE TABLE `jogo` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `categoria` varchar(40) COLLATE utf8_bin NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO jogoteca.usuario (id, nome, senha) VALUES (%s, %s, %s)',
      [
            ('gustavo', 'Gustavo Steinmetz', 'flask'),
            ('nico', 'Nico Steppat', '7a1'),
            ('marcos', 'Marcos', 'aurelio')
      ])

cursor.execute('select * from jogoteca.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO jogoteca.jogo (nome, categoria, console) VALUES (%s, %s, %s)',
      [
            ('Counter Strike', 'FPS', 'PC'),
            ('Crash Team Racing', 'Corrida', 'PS4'),
            ('Fifa', 'Esporte', 'PS4'),
            ('Empire Earth', 'Estrategia', 'PC'),
            ('Super Mario Kart', 'Corrida', 'SNES'),
            ('World of Warcraft', 'MMORPG', 'PC'),
      ])

cursor.execute('select * from jogoteca.jogo')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando se não nada tem efeito
conn.commit()
cursor.close()