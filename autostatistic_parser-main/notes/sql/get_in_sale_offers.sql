SELECT
    `offer` . `id`,
    `offer` . `url`,
    `offer` . `price`,
    `offer` . `createdon`,
    `offer` . `checkedon`,
    `offer` . `inspections_number`,
    `tracking` . `price` AS `tracking_price`
FROM
    `offers_list` AS `offer`
LEFT JOIN
    `offers_tracking` AS `tracking`
ON
    `tracking` . `item_id` = `offer` . `id` AND
    `tracking` . `checkedon` = (
        (
          SELECT
            MAX(`inner_tracking` . `checkedon`)
          FROM
            `offers_tracking` AS `inner_tracking`
          WHERE
            `inner_tracking` . `item_id` = `offer` . `id`
        )
    )
WHERE
    `offer` . `url` IS NOT NULL AND
    `offer` . `status` IS NULL AND
    `offer` . `region` = "Санкт-Петербург" AND
    `offer` . `createdon` > "2021-08-03 12:17:49"
ORDER BY
    `offer` . `id` DESC,
    `tracking` . `checkedon` DESC;
