SELECT
	dic.t_powiaty.nazdod OPIS_POWIATU,
	dic.t_powiaty.nazwa NAZWA_POWIATU
From dic.t_powiaty
WHERE dic.t_powiaty.okres='2014' and dic.t_powiaty.woj like 'Parametr%'