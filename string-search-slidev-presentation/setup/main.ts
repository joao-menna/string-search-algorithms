import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { defineAppSetup } from '@slidev/types'
import { faFileCode, faGaugeHigh, faChartLine } from '@fortawesome/free-solid-svg-icons'
import { faTerminal } from '@fortawesome/free-solid-svg-icons'
import { faFileImport } from '@fortawesome/free-solid-svg-icons'
import { faGears } from '@fortawesome/free-solid-svg-icons'
import { faSatelliteDish } from '@fortawesome/free-solid-svg-icons'
import { faSquarePollVertical } from '@fortawesome/free-solid-svg-icons'
import { faArrowRight } from '@fortawesome/free-solid-svg-icons'

library.add(
    faFileCode,
    faGaugeHigh,
    faChartLine,
    faTerminal,
    faFileImport,
    faGears,
    faSatelliteDish,
    faSquarePollVertical,
    faArrowRight,
)

export default defineAppSetup(({ app, router }) => {
    app.component('font-awesome-icon', FontAwesomeIcon)
})