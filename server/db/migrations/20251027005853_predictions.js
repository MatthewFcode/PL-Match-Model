/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export async function up(knex) {
  return knex.schema.createTable('predictions', (table) => {
    table.increments('id').primary()
    table.string('away_team')
    table.string('date')
    table.string('explanation')
    table.string('home_team')
    table.string('winning_team')
  })
}

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export async function down(knex) {
  return knex.schema.dropTable('predictions')
}
