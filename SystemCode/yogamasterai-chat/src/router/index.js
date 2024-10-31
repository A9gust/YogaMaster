import { createRouter, createWebHashHistory } from "vue-router";

import LoginIndex from "../components/LoginIndex.vue";
import ChatPage from "../components/ChatPage.vue";
import TestRecord from "../components/TestRecord.vue";

const router = createRouter({
  routes: [
    {
      path: "/",
      component: LoginIndex,
    },
    {
      path: "/ChatPage",
      component: ChatPage,
    },
    {
      path: "/LoginIndex",
      component: LoginIndex,
    },
    {
      path: "/TestRecord",
      component: TestRecord,
    },
  ],
  history: createWebHashHistory(),
});

export default router;
