import MotionResolver from 'motion-v/resolver'
import { defineConfig } from 'vite'

export default defineConfig({
    slidev: {
        components: {
            resolvers: [
                MotionResolver(),
            ],
        },
    },
})