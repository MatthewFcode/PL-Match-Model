/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export async function seed(knex) {
  // Deletes ALL existing entries
  await knex('teams').del()
  await knex('teams').insert([
    { team_name: 'rowValue1', team_logo: '' },
    { team_name: 'rowValue2', team_logo: '' },
    { team_name: 'rowValue3', team_logo: '' },
  ])
}
