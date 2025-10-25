/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export async function up(knex) {
  return knex.schema.createTable('teams', (table) => {
    table.increments('id').primary()
    table.string('team_name')
    table.string('team_logo')
    table.float('stadium_lat')
    table.float('stadium_lng')
  })
}

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export async function down(knex) {
  return knex.schema.dropTable('teams')
}
