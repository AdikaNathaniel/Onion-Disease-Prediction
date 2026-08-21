import type { Metadata } from "next";
import { GraduationCap, Mail, Smartphone } from "lucide-react";
import Reveal from "@/components/Reveal";
import ContactForm from "@/components/ContactForm";
import HeroCarousel from "@/components/HeroCarousel";
import TypingText from "@/components/TypingText";
import { CONTACT_HERO_IMAGES, CONTACT_TYPING_PHRASES, PLAY_STORE_URL } from "@/lib/data";

export const metadata: Metadata = {
  title: "Contact Us — OnionGuard",
  description: "Get in touch with the OnionGuard team.",
};

export default function ContactPage() {
  return (
    <div>
      <HeroCarousel images={CONTACT_HERO_IMAGES}>
        <Reveal className="px-5 py-10 text-center sm:px-8">
          <span className="text-xs font-semibold uppercase tracking-widest text-brand-200">
            Contact us
          </span>
          <h1 className="font-display mt-3 whitespace-nowrap text-[clamp(0px,calc(12px+2.46vw),2.75rem)] font-extrabold text-white">
            We&apos;d love to hear from you
          </h1>
          <div className="mx-auto mt-4 flex min-h-14 max-w-3xl items-start justify-center">
            <TypingText
              phrases={CONTACT_TYPING_PHRASES}
              className="text-base leading-relaxed text-white/85 sm:text-lg"
            />
          </div>
        </Reveal>
      </HeroCarousel>

      <section className="bg-white">
        <div className="mx-auto grid max-w-5xl gap-12 px-5 pb-24 sm:px-8 lg:grid-cols-5">
          <Reveal className="lg:col-span-3">
            <ContactForm />
          </Reveal>

          <Reveal delay={0.1} className="lg:col-span-2">
            <div className="space-y-6 rounded-2xl border border-border bg-surface p-6">
              <div className="flex gap-3">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-100 text-brand-700">
                  <Smartphone size={18} />
                </span>
                <div>
                  <h3 className="text-sm font-semibold text-brand-950">Get the app</h3>
                  <p className="mt-1 text-sm text-muted">
                    OnionGuard is live on the Google Play Store.
                  </p>
                  <a
                    href={PLAY_STORE_URL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 inline-block text-sm font-semibold text-brand-700 hover:text-brand-600"
                  >
                    Download now →
                  </a>
                </div>
              </div>

              <div className="flex gap-3">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-100 text-brand-700">
                  <GraduationCap size={18} />
                </span>
                <div>
                  <h3 className="text-sm font-semibold text-brand-950">Academic project</h3>
                  <p className="mt-1 text-sm text-muted">
                    Built by the Nkabom Honours Team at the University of Ghana.
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-100 text-brand-700">
                  <Mail size={18} />
                </span>
                <div>
                  <h3 className="text-sm font-semibold text-brand-950">Email</h3>
                  <p className="mt-1 text-sm text-muted">
                    Use the form and we&apos;ll route your message to the right team member.
                  </p>
                </div>
              </div>
            </div>
          </Reveal>
        </div>
      </section>
    </div>
  );
}
