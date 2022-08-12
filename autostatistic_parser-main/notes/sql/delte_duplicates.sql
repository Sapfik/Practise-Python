DELETE
  `offers_list`
FROM
	`offers_list`
LEFT OUTER JOIN
	(SELECT MIN(`id`) AS `id`, `url` FROM `offers_list` GROUP BY `url`) AS `tmp`
ON
	`offers_list`.`id` = `tmp`.`id`
WHERE
	`tmp`.`id` IS NULL;
