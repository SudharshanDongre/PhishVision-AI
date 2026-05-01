"""Contact & Support modal for the PhishVision Help section."""

from __future__ import annotations

from urllib.parse import quote

import streamlit as st


def _close_support_modal() -> None:
    st.session_state.show_support_modal = False


def _build_mailto(recipient: str, subject: str, body: str) -> str:
    return f"mailto:{recipient}?subject={quote(subject)}&body={quote(body)}"


def _render_support_body(support_email: str, support_hours: str, support_phone: str | None) -> None:
    st.markdown(
        """
        <style>
        dialog {
            border: 1px solid rgba(0, 212, 255, 0.22) !important;
            border-radius: 24px !important;
            background: linear-gradient(160deg, rgba(7,16,32,0.98), rgba(11,23,48,0.96)) !important;
            box-shadow: 0 28px 90px rgba(2, 6, 23, 0.58) !important;
            padding: 0 !important;
            overflow: hidden !important;
            width: min(860px, calc(100vw - 32px)) !important;
            max-width: min(860px, calc(100vw - 32px)) !important;
        }
        dialog::backdrop {
            background: rgba(2, 6, 23, 0.72) !important;
            backdrop-filter: blur(10px) saturate(115%) !important;
        }
        .support-shell {
            max-width: 860px;
            margin: 0 auto;
        }
        .support-panel-wrap {
            padding: 18px;
            color: #e2e8f0;
            font-family: Inter, sans-serif;
        }
        .support-title {
            font-family: 'Orbitron', monospace;
            color: #00d4ff;
            letter-spacing: 1.5px;
            font-size: 1.1rem;
            margin-bottom: 8px;
            text-transform: uppercase;
        }
        .support-sub {
            color: #94a3b8;
            font-size: 0.92rem;
            margin-bottom: 12px;
        }
        .support-card {
            border: 1px solid rgba(0, 212, 255, 0.16);
            border-radius: 18px;
            background: linear-gradient(160deg, rgba(7, 16, 32, 0.92), rgba(11, 23, 48, 0.88));
            padding: 16px;
            height: 100%;
        }
        .support-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 999px;
            border: 1px solid rgba(0, 212, 255, 0.18);
            background: rgba(0, 212, 255, 0.08);
            color: #7dd3fc;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        .support-metric {
            margin-top: 12px;
            padding: 12px 14px;
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.14);
            background: rgba(15, 23, 42, 0.65);
        }
        .support-label {
            color: #94a3b8;
            font-size: 0.74rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            font-weight: 700;
        }
        .support-value {
            margin-top: 4px;
            color: #f8fbff;
            font-size: 0.92rem;
            font-weight: 600;
            line-height: 1.45;
        }
        .support-list {
            margin: 12px 0 0 0;
            padding: 0 0 0 18px;
            color: #cbd5e1;
            font-size: 0.88rem;
            line-height: 1.65;
        }
        .support-list li { margin-bottom: 6px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="support-panel-wrap"><div class="support-shell">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;"><div style="background:#3b82f6;border-radius:8px;width:34px;height:34px;display:flex;align-items:center;justify-content:center;">❓</div><div style="font-family:Inter,sans-serif;color:#e2e8f0;font-weight:700;font-size:1.1rem;">Contact & Support</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="support-title">Help Center</div><div class="support-sub">Reach the PhishVision team for bugs, threat intelligence reports, or technical assistance without changing any existing workflow.</div>', unsafe_allow_html=True)

    left, right = st.columns([1.1, 0.9], gap="large")
    with left:
        st.markdown('<div class="support-card">', unsafe_allow_html=True)
        st.markdown('<div class="support-badge">Support Overview</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="support-metric">
                <div class="support-label">Support Email</div>
                <div class="support-value">{support_email}</div>
            </div>
            <div class="support-metric">
                <div class="support-label">Response Availability</div>
                <div class="support-value">{support_hours}</div>
            </div>
            <div class="support-metric">
                <div class="support-label">Phone</div>
                <div class="support-value">{support_phone or 'Available on request via email'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <ul class="support-list">
                <li>Request a threat intelligence report or review suspicious activity.</li>
                <li>Report bugs, UI issues, or authentication problems.</li>
                <li>Ask for technical assistance with setup, deployment, or usage.</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

        st.link_button(
            "Send Email",
            _build_mailto(
                support_email,
                "PhishVision Support Request",
                "Hello PhishVision Support,\n\nI need assistance with: \n\nThank you.",
            ),
            use_container_width=True,
            type="primary",
            icon="✉️",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="support-card">', unsafe_allow_html=True)
        st.markdown('<div class="support-badge">Quick Contact Form</div>', unsafe_allow_html=True)
        with st.form("support_contact_form", clear_on_submit=False):
            name = st.text_input("Name", key="support_name", placeholder="Your name")
            email = st.text_input("Email", key="support_email", placeholder="you@example.com")
            subject = st.text_input("Subject", key="support_subject", placeholder="Bug report / Intel request / Technical help")
            message = st.text_area("Message", key="support_message", placeholder="Describe the issue or request...", height=140)
            topic = st.selectbox(
                "Reason",
                ["Bug report", "Threat intelligence report", "Technical assistance"],
                key="support_reason",
            )
            submit = st.form_submit_button("Prepare Email", use_container_width=True)

        if submit:
            subject_value = subject.strip() or topic
            body_lines = [
                f"Name: {name.strip() or 'N/A'}",
                f"Email: {email.strip() or 'N/A'}",
                f"Reason: {topic}",
                "",
                message.strip() or "No additional details provided.",
            ]
            st.link_button(
                "Open Email Client",
                _build_mailto(support_email, f"PhishVision - {subject_value}", "\n".join(body_lines)),
                use_container_width=True,
                type="primary",
                icon="✉️",
            )

        st.caption("The form only prepares your email; it does not change authentication or other app workflows.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)


def render_contact_support_panel(
    mode: str = "help",
    support_email: str = "support@phishvision.ai",
    support_hours: str = "Mon-Fri, 9:00 AM-6:00 PM IST",
    support_phone: str | None = None,
) -> None:
    if not st.session_state.get("show_support_modal"):
        return

    if hasattr(st, "dialog"):
        @st.dialog("PhishVision Support", width="large", dismissible=True, icon="❓", on_dismiss=_close_support_modal)
        def _support_dialog():
            _render_support_body(support_email, support_hours, support_phone)

        _support_dialog()
        return

    _render_support_body(support_email, support_hours, support_phone)