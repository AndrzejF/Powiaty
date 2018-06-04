SELECT
	dic.t_wojew.woj WOJ,
	dic.t_wojew.nazwa WOJEWODZTWO
From dic.t_wojew
Where dic.t_wojew.woj<>'00'
