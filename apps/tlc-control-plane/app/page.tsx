import { ControlPlaneShell } from "@/components/control-plane-shell";
import { ExecutionPane } from "@/components/execution-pane";
import { StatusPanel } from "@/components/status-panel";
import { SystemGraphPanel } from "@/components/system-graph-panel";
import { VerificationStream } from "@/components/verification-stream";

export default function HomePage() {
  return (
    <ControlPlaneShell>
      <SystemGraphPanel />
      <StatusPanel />
      <ExecutionPane />
      <VerificationStream />
    </ControlPlaneShell>
  );
}
