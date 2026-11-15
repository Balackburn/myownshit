export const meta = {
  name: 'review-draft',
  description: 'Two independent critics (animation director, art director) review a story draft from its evidence folder',
  whenToUse: 'After a draft is rendered and its critic folder is built (build.sh stills, then build.sh): args = { name, folder, round }',
  phases: [
    { title: 'Revue', detail: 'animation and art direction, in parallel, blind to each other' },
  ],
}

const folder = args.folder
const roles = [
  { key: 'anim', label: 'animation' },
  { key: 'art', label: 'direction artistique' },
]

phase('Revue')
const reports = (await parallel(roles.map(r => () => agent(
  `Your complete brief is in this file; read it in full first and follow it exactly: ${folder}/prompt_${r.key}.txt
Your scratch directory: ${folder}-frames/${r.key}
Your final answer must be the complete report itself, in the exact format the brief asks for (it is saved verbatim as the review of record), starting with the "Score:" line.`,
  { label: `${args.name} r${args.round}: ${r.label}`, phase: 'Revue', agentType: 'general-purpose' }
).then(text => text && { role: r.key, report: text })))).filter(Boolean)

const score = t => { const m = /Score:\s*([0-9]+(?:[.,][0-9]+)?)/.exec(t || ''); return m ? parseFloat(m[1].replace(',', '.')) : null }
const summary = reports.map(r => `${r.role} ${score(r.report)}`).join(' ; ')
log(`${args.name} revue ${args.round} : ${summary}`)
if (reports.length < roles.length) log(`attention : ${roles.length - reports.length} critique(s) sans rapport`)
return { name: args.name, round: args.round, folder, scores: Object.fromEntries(reports.map(r => [r.role, score(r.report)])), reports }
