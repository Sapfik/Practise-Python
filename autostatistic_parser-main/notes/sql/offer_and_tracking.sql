SELECT
  `tracking` . `item_id`,
  `tracking` . `price` AS `tracking_price`,
  `tracking` . `checkedon`,
  `offer` . `url`,
  `offer` . `status`,
  `offer` . `price` AS `first_price`,
  `offer` . `sale_time`,
  `offer` . `inspections_number`
FROM
  `offers_tracking` AS `tracking`
LEFT JOIN
  `offers_list` AS `offer`
ON
  `offer` . `id` = `tracking` . `item_id`
ORDER BY
  `tracking` . `checkedon` DESC;
