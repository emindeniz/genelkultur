Drop table [dbo].[questions];

CREATE TABLE [dbo].[questions] (
ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
,
question VARCHAR(MAX) NOT NULL,
  answer VARCHAR(MAX) NOT NULL,
  score INT CHECK (score>= 10 AND score<= 200) NOT NULL,
qtype VARCHAR(MAX) NOT NULL,
category VARCHAR(MAX) NOT NULL
);

insert into [dbo].[questions] (question, answer, score, qtype, category)
values ('Mersin''de ''Eshab-i Kehf'' olarak bilinen mağaranın diger adıdır ... UYURLAR MAĞARASI', 'yedi',30,'gercek', 'coğrafya')

insert into [dbo].[questions] (question, answer, score, qtype, category)
values ('Birine her ay görevi karşılığı ödenen paradır', 'maaş',30,'gercek', 'çalışma hayatı')

insert into [dbo].[questions] (question, answer, score, qtype, category)
values ('Genellikle sokaktaki satıcıların kullandığı üzerine ürünlerin konduğu nesnedir', 'tabla',40,'gercek', 'alış veriş')

insert into [dbo].[questions] (question, answer, score, qtype, category)
values ('Bir maddenin ısı yoluyla gaz halden doğrudan katı hale dönüşmesidir', 'kırağılaşma',90,'gercek', 'fizik')





SELECT top 1 * FROM [dbo].[questions]
WHERE id >= RAND() * (SELECT MAX(id) FROM [dbo].[questions])
order by id;

Drop table [dbo].[user];

CREATE TABLE [dbo].[user] (
  id NVARCHAR PRIMARY KEY,
  name NVARCHAR(MAX) NOT NULL,
  email VARCHAR UNIQUE NOT NULL,
  profile_pic VARCHAR(MAX) NOT NULL,
  questions_asked INT NOT NULL DEFAULT 0,
  questions_correct INT NOT NULL DEFAULT 0,
  questions_incorrect INT NOT NULL DEFAULT 0
);