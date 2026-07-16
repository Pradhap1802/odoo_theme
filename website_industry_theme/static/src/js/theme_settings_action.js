/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

class IndustryThemeSettingsAction extends Component {
    static template = "website_industry_theme.ThemeSettingsAction";

    setup() {
        this.notification = useService("notification");
        this.action = useService("action");

        this.state = useState({
            websites: [],
            themes: [],
            activeWebsiteId: null,
            activeThemeId: null,
            selectedThemeId: null,
            viewportMode: "desktop", // desktop, tablet, mobile
            iframeUrl: "/",
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        try {
            // Load websites list
            const websites = await rpc("/web/dataset/call_kw/website/search_read", {
                model: "website",
                method: "search_read",
                args: [[], ["id", "name", "industry_theme_id", "domain"]],
                kwargs: {}
            });

            // Load industry themes
            const themes = await rpc("/web/dataset/call_kw/industry.theme/search_read", {
                model: "industry.theme",
                method: "search_read",
                args: [[["active", "=", true]], ["id", "name", "code", "category_id", "palette_id", "font_id", "layout_id"]],
                kwargs: {}
            });

            // Fetch details for palette, font, and layout
            for (let theme of themes) {
                const palette = await rpc("/web/dataset/call_kw/industry.theme.palette/search_read", {
                    model: "industry.theme.palette",
                    method: "search_read",
                    args: [[["id", "=", theme.palette_id[0]]], ["primary_color", "secondary_color", "accent_color", "bg_color"]],
                    kwargs: {}
                });
                theme.palette = palette[0] || {};

                const font = await rpc("/web/dataset/call_kw/industry.theme.font/search_read", {
                    model: "industry.theme.font",
                    method: "search_read",
                    args: [[["id", "=", theme.font_id[0]]], ["font_family", "font_url"]],
                    kwargs: {}
                });
                theme.font = font[0] || {};

                const layout = await rpc("/web/dataset/call_kw/industry.theme.layout/search_read", {
                    model: "industry.theme.layout",
                    method: "search_read",
                    args: [[["id", "=", theme.layout_id[0]]], ["border_radius", "button_style", "shadow_style"]],
                    kwargs: {}
                });
                theme.layout = layout[0] || {};
            }

            this.state.websites = websites;
            this.state.themes = themes;

            if (websites.length > 0) {
                this.state.activeWebsiteId = websites[0].id;
                this.state.activeThemeId = websites[0].industry_theme_id ? websites[0].industry_theme_id[0] : null;
                this.state.selectedThemeId = this.state.activeThemeId || (themes.length > 0 ? themes[0].id : null);
            }
            this.updateIframeUrl();
        } catch (error) {
            console.error("Failed to load Odoo Theme Settings Action data", error);
        }
    }

    get selectedTheme() {
        return this.state.themes.find(t => t.id === Number(this.state.selectedThemeId)) || null;
    }

    updateIframeUrl() {
        const themeId = this.state.selectedThemeId;
        this.state.iframeUrl = `/?preview_theme_id=${themeId}&t=${Date.now()}`;
    }

    onThemeChange(ev) {
        this.state.selectedThemeId = Number(ev.target.value);
        this.updateIframeUrl();
    }

    onWebsiteChange(ev) {
        const webId = Number(ev.target.value);
        this.state.activeWebsiteId = webId;
        const web = this.state.websites.find(w => w.id === webId);
        this.state.activeThemeId = web.industry_theme_id ? web.industry_theme_id[0] : null;
        this.state.selectedThemeId = this.state.activeThemeId || (this.state.themes.length > 0 ? this.state.themes[0].id : null);
        this.updateIframeUrl();
    }

    setViewport(mode) {
        this.state.viewportMode = mode;
    }

    async applyTheme() {
        if (!this.state.activeWebsiteId || !this.state.selectedThemeId) return;
        try {
            await rpc("/web/dataset/call_kw/website/write", {
                model: "website",
                method: "write",
                args: [[this.state.activeWebsiteId], { industry_theme_id: this.state.selectedThemeId }],
                kwargs: {}
            });
            this.state.activeThemeId = this.state.selectedThemeId;
            this.notification.add("Theme applied successfully to website!", {
                type: "success",
                title: "Theme Applied",
            });
            this.updateIframeUrl();
        } catch (error) {
            this.notification.add("Failed to apply theme.", {
                type: "danger",
            });
        }
    }

    async duplicateSelectedTheme() {
        if (!this.state.selectedThemeId) return;
        try {
            const res = await rpc("/web/dataset/call_kw/industry.theme/action_duplicate", {
                model: "industry.theme",
                method: "action_duplicate",
                args: [[this.state.selectedThemeId]],
                kwargs: {}
            });
            this.notification.add("Theme duplicated successfully!", {
                type: "success",
            });
            await this.loadData();
        } catch (error) {
            this.notification.add("Duplication failed.", {
                type: "danger",
            });
        }
    }

    async exportSelectedTheme() {
        if (!this.state.selectedThemeId) return;
        try {
            const actionResult = await rpc("/web/dataset/call_kw/industry.theme/action_export_theme", {
                model: "industry.theme",
                method: "action_export_theme",
                args: [[this.state.selectedThemeId]],
                kwargs: {}
            });
            this.action.doAction(actionResult);
        } catch (error) {
            this.notification.add("Export failed.", {
                type: "danger",
            });
        }
    }

    async resetSelectedTheme() {
        if (!this.state.selectedThemeId) return;
        if (confirm("Reset current colors and layouts variables to theme seed defaults?")) {
            try {
                await rpc("/web/dataset/call_kw/industry.theme/action_reset", {
                    model: "industry.theme",
                    method: "action_reset",
                    args: [[this.state.selectedThemeId]],
                    kwargs: {}
                });
                this.notification.add("Theme styles reset to default.", {
                    type: "success",
                });
                await this.loadData();
                this.updateIframeUrl();
            } catch (error) {
                this.notification.add("Reset failed.", {
                    type: "danger",
                });
            }
        }
    }
}

registry.category("actions").add("website_industry_theme.theme_settings", IndustryThemeSettingsAction);
