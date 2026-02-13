"""
Parameter Validator for Testing Framework
==========================================
Validates that parameter changes in the teaching agent are accurate:
- Teacher's claims match actual state changes
- Parameters are within valid ranges
- URLs contain correct parameter values
- Conversation accurately describes parameter modifications
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import urlparse, parse_qs


class ParameterValidation:
    """Results of parameter validation for a single turn."""
    
    def __init__(self):
        self.turn_number: int = 0
        self.passed: bool = True
        self.issues: List[str] = []
        self.warnings: List[str] = []
        
        # What was validated
        self.claimed_changes: List[Dict[str, Any]] = []  # What teacher claimed
        self.actual_changes: List[Dict[str, Any]] = []   # What actually changed in state
        self.url_params: Dict[str, str] = {}             # Parameters in simulation URL
        
        # Validation results
        self.claim_matches_state: bool = True
        self.state_matches_url: bool = True
        self.params_in_range: bool = True
        
    def add_issue(self, message: str):
        """Add a critical validation failure."""
        self.issues.append(message)
        self.passed = False
        
    def add_warning(self, message: str):
        """Add a warning (non-critical issue)."""
        self.warnings.append(message)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for reports."""
        return {
            "turn": self.turn_number,
            "passed": self.passed,
            "issues": self.issues,
            "warnings": self.warnings,
            "claimed_changes": self.claimed_changes,
            "actual_changes": self.actual_changes,
            "url_params": self.url_params,
            "validation_checks": {
                "claim_matches_state": self.claim_matches_state,
                "state_matches_url": self.state_matches_url,
                "params_in_range": self.params_in_range,
            }
        }


class ParameterValidator:
    """Validates parameter changes during testing."""
    
    def __init__(self, simulation_id: str):
        """
        Initialize validator for a specific simulation.
        
        Args:
            simulation_id: The simulation being tested.
        """
        self.simulation_id = simulation_id
        self.validation_history: List[ParameterValidation] = []
        
        # Load simulation config
        from simulations_config import get_simulation
        self.sim_config = get_simulation(simulation_id)
        if not self.sim_config:
            raise ValueError(f"Unknown simulation: {simulation_id}")
            
        self.param_info = self.sim_config.get("parameter_info", {})
        
    def validate_turn(
        self,
        turn_number: int,
        teacher_message: str,
        state: Dict[str, Any],
        previous_params: Optional[Dict[str, Any]] = None
    ) -> ParameterValidation:
        """
        Validate parameter accuracy for a single turn.
        
        Args:
            turn_number: Current turn number.
            teacher_message: What the teacher said.
            state: Current agent state.
            previous_params: Parameters from previous turn (for detecting changes).
            
        Returns:
            ParameterValidation with results.
        """
        validation = ParameterValidation()
        validation.turn_number = turn_number
        
        current_params = state.get("current_params", {})
        param_history = state.get("parameter_history", [])
        simulation_url = state.get("simulation_url", "")
        
        # 1. Extract claimed parameter changes from teacher message
        validation.claimed_changes = self._extract_parameter_claims(teacher_message)
        
        # 2. Get actual parameter changes from state
        if previous_params:
            validation.actual_changes = self._detect_actual_changes(
                previous_params, current_params
            )
        elif param_history:
            # Use most recent history entry if no previous params
            validation.actual_changes = [param_history[-1]]
        
        # 3. Extract parameters from URL
        validation.url_params = self._extract_url_params(simulation_url)
        
        # 4. Validate: Do claimed changes match actual changes?
        validation.claim_matches_state = self._validate_claims_vs_state(
            validation.claimed_changes,
            validation.actual_changes,
            current_params,
            validation
        )
        
        # 5. Validate: Does state match URL?
        validation.state_matches_url = self._validate_state_vs_url(
            current_params,
            validation.url_params,
            validation
        )
        
        # 6. Validate: Are parameters in valid ranges?
        validation.params_in_range = self._validate_parameter_ranges(
            current_params,
            validation
        )
        
        self.validation_history.append(validation)
        return validation
        
    def _extract_parameter_claims(self, teacher_message: str) -> List[Dict[str, Any]]:
        """
        Extract parameter change claims from teacher's message using patterns.
        
        Returns:
            List of dicts with {parameter, value, confidence}.
        """
        claims = []
        
        # Common patterns for parameter mentions
        patterns = [
            # "set X to Y", "change X to Y", "adjust X to Y"
            r'(?:set|change|adjust|update)\s+(\w+(?:\s+\w+)*?)\s+to\s+(\d+\.?\d*)',
            # "X is now Y", "X = Y"
            r'(\w+(?:\s+\w+)*?)\s+(?:is now|=)\s+(\d+\.?\d*)',
            # "increase/decrease X to Y"
            r'(?:increase|decrease)\s+(\w+(?:\s+\w+)*?)\s+to\s+(\d+\.?\d*)',
            # "make X Y"
            r'make\s+(?:the\s+)?(\w+(?:\s+\w+)*?)\s+(\d+\.?\d*)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, teacher_message, re.IGNORECASE)
            for match in matches:
                param_name = match.group(1).strip().lower()
                param_value = match.group(2).strip()
                
                # Try to match to actual parameter names
                matched_param = self._match_parameter_name(param_name)
                if matched_param:
                    claims.append({
                        "parameter": matched_param,
                        "value": float(param_value) if '.' in param_value else int(param_value),
                        "raw_text": match.group(0),
                        "confidence": "high"
                    })
        
        return claims
        
    def _match_parameter_name(self, text: str) -> Optional[str]:
        """
        Match text to actual parameter name in config.
        
        Args:
            text: Text from teacher message (e.g., "pendulum length", "speed").
            
        Returns:
            Actual parameter key from config, or None.
        """
        text_lower = text.lower().replace(" ", "").replace("_", "")
        
        for param_key in self.param_info.keys():
            param_lower = param_key.lower().replace("_", "")
            
            # Exact match
            if text_lower == param_lower:
                return param_key
                
            # Partial match (text contains param or vice versa)
            if text_lower in param_lower or param_lower in text_lower:
                return param_key
                
            # Check label too
            label = self.param_info[param_key].get("label", "").lower()
            label_clean = label.replace(" ", "").replace("_", "")
            if text_lower in label_clean or label_clean in text_lower:
                return param_key
        
        return None
        
    def _detect_actual_changes(
        self,
        previous_params: Dict[str, Any],
        current_params: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Detect which parameters actually changed between turns.
        
        Returns:
            List of dicts with {parameter, old_value, new_value}.
        """
        changes = []
        
        for param_key in current_params.keys():
            old_val = previous_params.get(param_key)
            new_val = current_params.get(param_key)
            
            if old_val != new_val:
                changes.append({
                    "parameter": param_key,
                    "old_value": old_val,
                    "new_value": new_val
                })
        
        return changes
        
    def _extract_url_params(self, simulation_url: str) -> Dict[str, str]:
        """Extract parameter values from simulation URL query string."""
        if not simulation_url:
            return {}
            
        parsed = urlparse(simulation_url)
        params = parse_qs(parsed.query)
        
        # parse_qs returns lists, convert to single values
        return {k: v[0] if v else "" for k, v in params.items()}
        
    def _validate_claims_vs_state(
        self,
        claims: List[Dict[str, Any]],
        actual_changes: List[Dict[str, Any]],
        current_params: Dict[str, Any],
        validation: ParameterValidation
    ) -> bool:
        """
        Validate that teacher's claims match actual state changes.
        
        Returns:
            True if all claims are accurate.
        """
        if not claims:
            return True  # No claims to validate
            
        all_match = True
        
        for claim in claims:
            param = claim["parameter"]
            claimed_value = claim["value"]
            current_value = current_params.get(param)
            
            # Check if claimed value matches current state
            if current_value is None:
                validation.add_issue(
                    f"Teacher claimed to set '{param}' to {claimed_value}, "
                    f"but parameter not found in state"
                )
                all_match = False
            elif current_value != claimed_value:
                # Check if values are close enough (for floats)
                if isinstance(current_value, (int, float)) and isinstance(claimed_value, (int, float)):
                    if abs(current_value - claimed_value) < 0.01:
                        continue  # Close enough
                
                validation.add_issue(
                    f"Parameter mismatch: Teacher claimed '{param}' = {claimed_value}, "
                    f"but state shows {current_value}"
                )
                all_match = False
            
            # Check if this parameter actually changed
            param_changed = any(
                change["parameter"] == param
                for change in actual_changes
            )
            
            if not param_changed:
                validation.add_warning(
                    f"Teacher mentioned changing '{param}' to {claimed_value}, "
                    f"but no change detected in parameter_history"
                )
        
        return all_match
        
    def _validate_state_vs_url(
        self,
        current_params: Dict[str, Any],
        url_params: Dict[str, str],
        validation: ParameterValidation
    ) -> bool:
        """
        Validate that URL parameters match state parameters.
        
        Returns:
            True if URL matches state.
        """
        if not url_params:
            validation.add_warning("No URL parameters found in simulation_url")
            return True  # Not a failure, might be first turn
            
        all_match = True
        
        for param_key, state_value in current_params.items():
            # Get corresponding URL parameter key
            param_info = self.param_info.get(param_key, {})
            url_key = param_info.get("url_key", param_key)
            
            url_value = url_params.get(url_key)
            
            if url_value is None:
                validation.add_warning(
                    f"Parameter '{param_key}' in state but not in URL"
                )
                continue
                
            # Convert URL string to same type as state value
            try:
                if isinstance(state_value, int):
                    url_value_converted = int(url_value)
                elif isinstance(state_value, float):
                    url_value_converted = float(url_value)
                else:
                    url_value_converted = url_value
                    
                if state_value != url_value_converted:
                    validation.add_issue(
                        f"URL mismatch: State has '{param_key}' = {state_value}, "
                        f"but URL has {url_value}"
                    )
                    all_match = False
            except ValueError:
                validation.add_issue(
                    f"URL parameter '{url_key}' has invalid value: {url_value}"
                )
                all_match = False
        
        return all_match
        
    def _validate_parameter_ranges(
        self,
        current_params: Dict[str, Any],
        validation: ParameterValidation
    ) -> bool:
        """
        Validate that all parameters are within valid ranges.
        
        Returns:
            True if all parameters in valid ranges.
        """
        all_valid = True
        
        for param_key, param_value in current_params.items():
            param_info = self.param_info.get(param_key)
            if not param_info:
                continue
                
            min_val = param_info.get("min")
            max_val = param_info.get("max")
            
            if min_val is not None and param_value < min_val:
                validation.add_issue(
                    f"Parameter '{param_key}' = {param_value} is below minimum {min_val}"
                )
                all_valid = False
                
            if max_val is not None and param_value > max_val:
                validation.add_issue(
                    f"Parameter '{param_key}' = {param_value} is above maximum {max_val}"
                )
                all_valid = False
        
        return all_valid
        
    def get_summary(self) -> Dict[str, Any]:
        """
        Get overall validation summary for the entire test session.
        
        Returns:
            Summary dict with pass rates and issue counts.
        """
        total_turns = len(self.validation_history)
        passed_turns = sum(1 for v in self.validation_history if v.passed)
        
        total_issues = sum(len(v.issues) for v in self.validation_history)
        total_warnings = sum(len(v.warnings) for v in self.validation_history)
        
        total_claims = sum(len(v.claimed_changes) for v in self.validation_history)
        total_actual_changes = sum(len(v.actual_changes) for v in self.validation_history)
        
        return {
            "simulation_id": self.simulation_id,
            "total_turns_validated": total_turns,
            "turns_passed": passed_turns,
            "turns_failed": total_turns - passed_turns,
            "pass_rate": passed_turns / total_turns if total_turns > 0 else 0.0,
            "total_issues": total_issues,
            "total_warnings": total_warnings,
            "total_parameter_claims": total_claims,
            "total_actual_changes": total_actual_changes,
            "validation_history": [v.to_dict() for v in self.validation_history]
        }
        
    def print_summary(self):
        """Print human-readable validation summary."""
        summary = self.get_summary()
        
        print("\n" + "="*70)
        print("🔍 PARAMETER VALIDATION SUMMARY")
        print("="*70)
        print(f"  Simulation:          {summary['simulation_id']}")
        print(f"  Turns Validated:     {summary['total_turns_validated']}")
        print(f"  Passed:              {summary['turns_passed']} ✅")
        print(f"  Failed:              {summary['turns_failed']} ❌")
        print(f"  Pass Rate:           {summary['pass_rate']*100:.1f}%")
        print(f"  Critical Issues:     {summary['total_issues']}")
        print(f"  Warnings:            {summary['total_warnings']}")
        print(f"  Parameter Claims:    {summary['total_parameter_claims']}")
        print(f"  Actual Changes:      {summary['total_actual_changes']}")
        
        if summary['total_issues'] > 0:
            print("\n❌ Issues Found:")
            for i, val in enumerate(self.validation_history):
                if val.issues:
                    print(f"\n  Turn {val.turn_number}:")
                    for issue in val.issues:
                        print(f"    • {issue}")
        
        if summary['total_warnings'] > 0:
            print("\n⚠️  Warnings:")
            for val in self.validation_history:
                if val.warnings:
                    print(f"\n  Turn {val.turn_number}:")
                    for warning in val.warnings:
                        print(f"    • {warning}")
        
        print("="*70)
